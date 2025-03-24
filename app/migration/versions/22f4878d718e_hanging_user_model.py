"""hanging user model

Revision ID: 22f4878d718e
Revises: bd85c3b4b4d6
Create Date: 2025-03-24 09:52:21.225716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22f4878d718e'
down_revision: Union[str, None] = 'bd85c3b4b4d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
