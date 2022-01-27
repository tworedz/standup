"""empty message

Revision ID: f8786aec0eca
Revises: a29f93d45d6f
Create Date: 2022-01-27 21:15:50.629246

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f8786aec0eca"
down_revision = "a29f93d45d6f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("warmup_summons", sa.Column("text", sa.String(), nullable=True))
    op.drop_column("warmup_summons", "summoner")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "warmup_summons", sa.Column("summoner", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_column("warmup_summons", "text")
    # ### end Alembic commands ###