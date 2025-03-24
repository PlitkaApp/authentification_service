"""change description to str

Revision ID: bd85c3b4b4d6
Revises: 4a51cdfa1c29
Create Date: 2025-03-23 21:13:11.064504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd85c3b4b4d6'
down_revision: Union[str, None] = '4a51cdfa1c29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_table('users')

