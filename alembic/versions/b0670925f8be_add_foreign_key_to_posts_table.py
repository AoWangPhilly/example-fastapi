"""add foreign key to posts table

Revision ID: b0670925f8be
Revises: 7d88ae1b0533
Create Date: 2021-12-29 13:06:49.888120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0670925f8be'
down_revision = '7d88ae1b0533'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
