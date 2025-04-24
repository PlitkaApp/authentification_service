from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.auth.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token, \
    get_refresh_token, decode_jwt, change_role, validate_token, \
    get_current_auth_user_for_refresh, get_current_active_user_id
from app.auth.token_schemas import TokenInfo
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import SUserRegister, SUserAuth, UpdateRolesRequest
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth import oauth2_scheme
from app.redis_blacklist import add_access_token_to_blacklist, add_refresh_token_to_blacklist


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


@router.get("/me/")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    await validate_token(token)
    payload = decode_jwt(token)
    return {'user_id': payload['sub'], 'user_roles': payload['role']}


@router.put("/roles/update", response_model=TokenInfo, response_model_exclude_none=True)
async def update_roles(
    request_data: UpdateRolesRequest,  # Данные из тела запроса
    refresh_token: str = Depends(get_refresh_token), # Токен из куков
    old_access_token: str = Depends(oauth2_scheme),  # access токен из ouath2
    user_id = Depends(get_current_active_user_id)
):
    await validate_token(refresh_token)
    await add_access_token_to_blacklist(user_id, old_access_token)  # Добавляем старый токен в blacklist
    await add_refresh_token_to_blacklist(user_id, refresh_token)    # Добавляем refresh токен в blacklist, чтобы пользователь перелогинился
    roles = await change_role(request_data.new_roles, user_id)
    if not roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось изменить роль")
    print(roles)
    access_token = create_access_token(user_id, roles)
    return TokenInfo(access_token=access_token)


@router.post("/logout")
async def logout_user(response: Response,
                      access_token: str = Depends(oauth2_scheme),
                      refresh_token: str = Depends(get_refresh_token),
                      user_id: User = Depends(get_current_active_user_id)):
    user_id = str(user_id)
    response.delete_cookie(key="refresh_token")                     # Чистим куки
    await add_refresh_token_to_blacklist(user_id, refresh_token)    # Добавляем refresh token в blacklist
    await add_access_token_to_blacklist(user_id, access_token)      # Добавляем access token в blacklist
    return {"message": "Успешный выход"}
