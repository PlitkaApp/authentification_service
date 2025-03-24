"""Trying to change description to nullable

Revision ID: 4a51cdfa1c29
Revises: df5b4af9f975
Create Date: 2025-03-23 21:11:27.538905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a51cdfa1c29'
down_revision: Union[str, None] = 'df5b4af9f975'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
