"""add last few columns to posts table

Revision ID: 75ca16380ff7
Revises: b0670925f8be
Create Date: 2021-12-29 13:42:05.550897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75ca16380ff7'
down_revision = 'b0670925f8be'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(),
                  nullable=False, server_default="TRUE")
    )

    op.add_column(
        "posts",
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text("NOW()"))
    )


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
