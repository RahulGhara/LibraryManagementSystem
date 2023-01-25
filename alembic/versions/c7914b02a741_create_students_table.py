"""Create Students Table

Revision ID: c7914b02a741
Revises: 90a7c059f8fa
Create Date: 2023-01-25 15:53:40.874455

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = 'c7914b02a741'
down_revision = '90a7c059f8fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "Student",
        sa.Column('StudentID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('RollNo', sa.String(100), nullable=False, unique=True),
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