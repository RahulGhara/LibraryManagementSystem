"""CreateBooksTable

Revision ID: 1dea04131b96
Revises: 
Create Date: 2022-11-30 13:40:12.921133

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1dea04131b96'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'StoreBooks',
        sa.Column('BookID', sa.Integer, primary_key=True, nullable=False),
        sa.Column('Name', sa.String(50), nullable=False),
        sa.Column('Author', sa.String(50)),
        sa.Column('Edition', sa.String(30)),
        sa.Column('Price', sa.Integer),
    )


def downgrade() -> None:
    op.drop_table('StoreBooks')
