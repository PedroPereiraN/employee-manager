"""creating user table2

Revision ID: 4c123aae814e
Revises: 477d714a7db2
Create Date: 2026-04-21 22:26:41.244146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c123aae814e'
down_revision: Union[str, Sequence[str], None] = '477d714a7db2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
