"""create book allocation table

Revision ID: 810c83f68593
Revises: b8305c73d38f
Create Date: 2022-12-06 15:14:48.495547

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# from Models.Student_6_12_22 import Students

# revision identifiers, used by Alembic.
revision = '810c83f68593'
down_revision = 'b8305c73d38f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'BookAllocationTable',
        sa.Column('StudentBookAllocationID', UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4),
        sa.Column('StudentID', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
        sa.Column('BookID', sa.Integer, nullable=False),
        sa.Column('IssueDate', sa.Date, nullable=False),
        sa.Column('IssueEndDate', sa.Date, nullable=False),
        sa.ForeignKeyConstraint(['StudentID'], ['Student.StudentID']),
        # sa.ForeignKeyConstraint(['BookID'], ['StoreBooks.BookID']),
    )


def downgrade() -> None:
    op.drop_table('BookAllocationTable')
