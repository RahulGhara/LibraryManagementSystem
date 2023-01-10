"""Creating admin table

Revision ID: f05ff86d6501
Revises: c972155681c3
Create Date: 2022-12-16 14:55:44.297276

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = 'f05ff86d6501'
down_revision = 'c972155681c3'
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
