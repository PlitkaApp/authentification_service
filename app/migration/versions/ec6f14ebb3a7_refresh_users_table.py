"""refresh users table

Revision ID: ec6f14ebb3a7
Revises: 22f4878d718e
Create Date: 2025-03-24 10:30:45.153556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec6f14ebb3a7'
down_revision: Union[str, None] = '22f4878d718e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    """Downgrade schema."""
    pass
