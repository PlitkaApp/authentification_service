from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from passlib.exc import InvalidTokenError

from app.config import get_auth_data

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.users.dao import UsersDAO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
http_bearer = HTTPBearer(auto_error=False)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, roles: list[str]) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {
        "sub": user_id,
        'role': roles,
        'token_type': 'access',
        'exp': expire,
        'iat': datetime.now(timezone.utc)
    }

    auth_data = get_auth_data()
    access_token = jwt.encode(payload, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return access_token


def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    payload = {
        "sub": user_id,
        "token_type": "refresh",
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }

    auth_data = get_auth_data()
    refresh_token = jwt.encode(payload, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return refresh_token


def decode_jwt(token):
    auth_data = get_auth_data()
    decoded = jwt.decode(token, auth_data['secret_key'], auth_data['algorithm'])
    return decoded


async def authenticate_user(login: str, password: str):
    user = await UsersDAO.find_one_or_none(login=login)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен отсутствует')
        payload = decode_jwt(token=token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Невалидный токен: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Ошибка аутентификации: {str(e)}"
        )
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload['token_type']
    if current_token_type == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Невалидный тип токена '{current_token_type}', ожидался '{token_type}'")


async def get_user_for_refresh(payload: dict = Depends(get_current_token_payload)) -> dict:
    validate_token_type(payload, 'refresh')
    user_id = payload['sub']
    user_roles = await UsersDAO.get_user_roles(int(user_id))
    if not user_roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Неавторизованный пользователь")
    return {'user_id': user_id, 'user_roles': user_roles}


