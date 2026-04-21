"""changing type to role

Revision ID: ceefbb8f137c
Revises: f13a44f8ccab
Create Date: 2026-04-21 22:19:53.099412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ceefbb8f137c'
down_revision: Union[str, Sequence[str], None] = 'f13a44f8ccab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
