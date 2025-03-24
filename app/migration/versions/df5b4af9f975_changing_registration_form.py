"""Changing registration form

Revision ID: df5b4af9f975
Revises: faee8155d2fc
Create Date: 2025-03-23 20:58:03.237791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df5b4af9f975'
down_revision: Union[str, None] = 'faee8155d2fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
