from enum import Enum

from pydantic import BaseModel, Field, validator, EmailStr
import re
from typing import List


class UpdateRolesRequest(BaseModel):
    new_roles: List[str]  # Список строковых ролей, например ["admin", "premium"]


class SUserRegister(BaseModel):
    login: str = Field(..., description="Email или номер телефона")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

    @validator("login")
    def validate_login(cls, value):
        if "@" in value:
            try:
                EmailStr._validate(value)
            except ValueError:
                raise ValueError("Некорректный email")
        else:
            if not re.match(r'^\+\d{5,15}$', value):
                raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value

class SUserAuth(BaseModel):
    login: str = Field(..., description="Email или номер телефона")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


    @validator("login")
    def validate_login(cls, value):
        if "@" in value:
            try:
                EmailStr._validate(value)
            except ValueError:
                raise ValueError("Некорректный email")
        else:
            if not re.match(r'^\+\d{5,15}$', value):
                raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value
