"""Create Admin Table

Revision ID: 9d4dd480a91c
Revises: f94ccd8d9af2
Create Date: 2023-01-25 16:08:20.416048

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = '9d4dd480a91c'
down_revision = 'f94ccd8d9af2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'Admin',
        sa.Column('ID',UUID(as_uuid=True),primary_key=True, default=uuid.uuid4),
        sa.Column('Name', sa.String(100)),
        sa.Column('ProfID',sa.String(50),unique=True),
        sa.Column('Password', sa.String(180), unique=True),
        sa.Column('Designation', sa.String(40), nullable=False),
        sa.Column('Email', sa.String(50),nullable=False),
        sa.Column('PhnNo', sa.BIGINT, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('Admin')
