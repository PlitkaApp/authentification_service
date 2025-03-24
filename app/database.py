from datetime import datetime
from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import mapped_column, DeclarativeBase, declared_attr, Mapped
from sqlalchemy import func

from app.config import get_db_url


DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]

# Базовый класс для всех моделей, использующий асинхронные атрибуты и декларативное определение моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True # Указывает, что это абстрактный класс и не будет создавать таблицу в базе данных

    # Декоратор для автоматического создания имени таблицы на основе имени класса
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]