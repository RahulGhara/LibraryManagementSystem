"""adding Book uuid column

Revision ID: c0f6345344b2
Revises: 1d9c6f1bba17
Create Date: 2023-01-25 19:07:56.355444

"""
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'c0f6345344b2'
down_revision = '1d9c6f1bba17'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('StoreBooks', sa.Column('BookUUID',UUID(as_uuid=True), primary_key=True, default=uuid.uuid4))


def downgrade() -> None:
    op.drop_column('StoreBooks', 'BookUUID')
