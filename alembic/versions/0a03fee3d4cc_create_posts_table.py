"""create posts table

Revision ID: 0a03fee3d4cc
Revises: 
Create Date: 2021-12-28 23:21:11.504664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a03fee3d4cc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table("posts")
