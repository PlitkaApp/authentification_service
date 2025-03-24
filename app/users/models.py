from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, Text
from app.database import Base


class User(Base):
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    place: Mapped[str] = mapped_column(nullable=True)        # Надо прописать отношения
    photo_URL: Mapped[str] = mapped_column(nullable=True)    # Надо прописать отношения

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_premium_user: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_tester: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_censor: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)