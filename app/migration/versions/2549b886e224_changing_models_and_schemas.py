"""changing models and schemas

Revision ID: 2549b886e224
Revises: ec6f14ebb3a7
Create Date: 2025-04-02 17:05:38.925987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2549b886e224'
down_revision: Union[str, None] = 'ec6f14ebb3a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
