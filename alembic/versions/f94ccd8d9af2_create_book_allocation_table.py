"""Create Book Allocation Table

Revision ID: f94ccd8d9af2
Revises: c7914b02a741
Create Date: 2023-01-25 16:01:49.571392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = 'f94ccd8d9af2'
down_revision = 'c7914b02a741'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'BookAllocationTable',
        sa.Column('StudentBookAllocationID', UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4),
        sa.Column('StudentID', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
        sa.Column('BookID', sa.String, nullable=False),
        sa.Column('IssueDate', sa.DateTime, nullable=False),
        sa.Column('IssueEndDate', sa.Date, nullable=False),
        sa.Column('ReturnTime', sa.DateTime),
        sa.ForeignKeyConstraint(['StudentID'], ['Student.StudentID']),
        # sa.ForeignKeyConstraint(['BookID'], ['StoreBooks.BookID']),
    )


def downgrade() -> None:
    op.drop_table('BookAllocationTable')