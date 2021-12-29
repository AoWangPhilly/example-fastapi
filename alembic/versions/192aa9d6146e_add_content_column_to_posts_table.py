"""add content column to posts table

Revision ID: 192aa9d6146e
Revises: 0a03fee3d4cc
Create Date: 2021-12-29 10:43:41.974525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '192aa9d6146e'
down_revision = '0a03fee3d4cc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
