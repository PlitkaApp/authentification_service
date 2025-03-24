"""Changing registration form

Revision ID: faee8155d2fc
Revises: 320e3fa9239a
Create Date: 2025-03-23 20:56:00.579865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'faee8155d2fc'
down_revision: Union[str, None] = '320e3fa9239a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    pass
