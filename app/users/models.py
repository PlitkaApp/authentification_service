from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, Text
from app.database import Base


class User(Base):
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    id: Mapped[int] = mapped_column(primary_key=True)

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_premium_user: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_tester: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_content_manager: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_system_analyst: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)