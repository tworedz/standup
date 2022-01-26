"""empty message

Revision ID: b2a3de8d4344
Revises: 5ddc31aac57e
Create Date: 2022-01-26 21:20:55.888745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b2a3de8d4344"
down_revision = "5ddc31aac57e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("groups", sa.Column("telegram_id", sa.BigInteger(), nullable=True))
    op.add_column("groups", sa.Column("title", sa.String(), nullable=True))
    op.create_unique_constraint(None, "groups", ["telegram_id"])
    op.create_unique_constraint(None, "user_groups", ["user_id", "group_id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user_groups", type_="unique")
    op.drop_constraint(None, "groups", type_="unique")
    op.drop_column("groups", "title")
    op.drop_column("groups", "telegram_id")
    # ### end Alembic commands ###
