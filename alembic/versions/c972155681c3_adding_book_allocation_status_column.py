"""adding book allocation status column

Revision ID: c972155681c3
Revises: 810c83f68593
Create Date: 2022-12-14 15:18:46.110425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c972155681c3'
down_revision = '810c83f68593'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('BookAllocationTable', sa.Column('BookAllocationStatus', sa.String(40)))


def downgrade() -> None:
    op.drop_column('BookAllocationTable', 'BookAllocationStatus')
