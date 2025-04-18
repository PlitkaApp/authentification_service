from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.auth.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token, \
    get_current_token_payload, get_user_for_refresh, get_refresh_token, decode_jwt, change_role, get_current_auth_user_for_refresh
from app.auth.token_schemas import TokenInfo
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth, UpdateRolesRequest
from fastapi.security import OAuth2PasswordRequestForm
from app.config import get_auth_data
from app.auth.auth import oauth2_scheme

from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(login=user_data.login)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегестрированы'}


@router.post("/login/", response_model=TokenInfo)
async def auth_user(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    check = await authenticate_user(login=form_data.username, password=form_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверный логин или пароль')
    user_roles = await UsersDAO.get_user_roles(check.id)
    access_token = create_access_token(str(check.id), user_roles)
    refresh_token = create_refresh_token(str(check.id))
    # Устанавливаем куки
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True
    )
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
async def refresh_access_token(user: dict = Depends(get_current_auth_user_for_refresh)):
    user_id = user['user_id']
    user_roles = user['user_roles']
    access_token = create_access_token(user_id, user_roles)

    return TokenInfo(
        access_token=access_token
    )


# @router.get('/me/')
# async def check_payload(payload: dict = Depends(get_current_token_payload)) -> dict:
#     token_type = payload['token_type']
#     if token_type != 'access':
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Неверный тип токена: {token_type} ожидался access")
#     return payload

@router.get("/me/")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    return {'user_id': payload['sub'], 'user_roles': payload['role']}


@router.put("/update", response_model=TokenInfo, response_model_exclude_none=True)
async def update_roles(
    request_data: UpdateRolesRequest,  # Данные из тела запроса
    refresh_token: str = Depends(get_refresh_token)  # Токен из куков/заголовков
):
    payload = decode_jwt(token=refresh_token)
    user_id = int(payload['sub'])  # Получаем user_id из токена
    roles = await change_role(user_id, request_data.new_roles)
    if not roles:
        raise HTTPException(status_code=400, detail="Не удалось изменить роль")
    print(roles)
    access_token = create_access_token(str(user_id), roles)
    return TokenInfo(access_token=access_token)