"""create student table

Revision ID: b8305c73d38f
Revises: 1dea04131b96
Create Date: 2022-12-05 14:51:50.963282

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'b8305c73d38f'
# revision = None
down_revision = '1dea04131b96'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "Student",
        sa.Column('StudentID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('RollNo', sa.Integer, nullable=False, unique=True),
        sa.Column('Name', sa.String(50), nullable=False),
        sa.Column('Department', sa.String(50), nullable=False),
        sa.Column('Semester', sa.String(30), nullable=False),
        sa.Column('PassoutYear', sa.Integer, nullable=False),
        sa.Column('UserID', sa.String(100), nullable=False, unique=True),
        sa.Column('Password', sa.String(1000), nullable=False, unique=True),
        sa.Column('Email', sa.String(80), nullable=False, unique=True),
        sa.Column('PhnNo', sa.BIGINT, nullable=False, unique=True),

    )


def downgrade() -> None:
    op.drop_table('Student')
