"""creating user table

Revision ID: 477d714a7db2
Revises: ceefbb8f137c
Create Date: 2026-04-21 22:25:00.400965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '477d714a7db2'
down_revision: Union[str, Sequence[str], None] = 'ceefbb8f137c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
