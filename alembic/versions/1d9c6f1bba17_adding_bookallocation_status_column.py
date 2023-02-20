"""adding BookAllocation Status Column

Revision ID: 1d9c6f1bba17
Revises: 9d4dd480a91c
Create Date: 2023-01-25 16:35:35.749011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d9c6f1bba17'
down_revision = '9d4dd480a91c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('BookAllocationTable', sa.Column('BookAllocationStatus', sa.String(50),nullable=False))


def downgrade() -> None:
    op.drop_column('BookAllocationTable', 'BookAllocationStatus')
