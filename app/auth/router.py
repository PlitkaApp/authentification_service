from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.auth.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token, \
    get_current_token_payload, get_user_for_refresh
from app.auth.token_schemas import TokenInfo
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth
from fastapi.security import OAuth2PasswordBearer
from app.config import get_auth_data
from app.auth.auth import http_bearer

from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(http_bearer)])


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
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(login=user_data.login, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверный логин или пароль')
    user_roles = await UsersDAO.get_user_roles(check.id)
    access_token = create_access_token(str(check.id), user_roles)
    refresh_token = create_refresh_token(str(check.id))
    # Устанавливаем куки
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True  # Только для HTTPS
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True
    )
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login/')

@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
async def refresh_access_token(payload: dict = Depends(get_user_for_refresh)):
    access_token = create_access_token(payload['user_id'], payload['user_roles'])

    return TokenInfo(
        access_token=access_token
    )

@router.get('/me/')
async def check_payload(payload: dict = Depends(get_current_token_payload)) -> dict:
    token_type = payload['token_type']
    if token_type != 'access':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Неверный тип токена: {token_type} ожидался access")
    return payload
