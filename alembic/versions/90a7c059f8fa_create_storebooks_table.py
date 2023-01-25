"""Create StoreBooks Table

Revision ID: 90a7c059f8fa
Revises: 
Create Date: 2023-01-25 15:37:31.845323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90a7c059f8fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'StoreBooks',
        sa.Column('BookID', sa.String(100), primary_key=True, nullable=False),
        sa.Column('Name', sa.String(50), nullable=False),
        sa.Column('Author', sa.String(50)),
        sa.Column('Edition', sa.String(30)),
        sa.Column('Price', sa.Integer),
        sa.Column('BooksAvailable', sa.Integer)
    )


def downgrade() -> None:
    op.drop_table('StoreBooks')
