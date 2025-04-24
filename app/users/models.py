from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, Text
from app.database import Base


class User(Base):
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    id: Mapped[int] = mapped_column(primary_key=True)
    active: Mapped[bool] = mapped_column(nullable=False, default=True, server_default=text('true'))

    user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    premium: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    tester: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    content_manager: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    system_analyst: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)