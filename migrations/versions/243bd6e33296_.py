"""empty message

Revision ID: 243bd6e33296
Revises: ccd83592482e
Create Date: 2021-01-23 21:41:36.538269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '243bd6e33296'
down_revision = 'ccd83592482e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('dishs', sa.String(), nullable=True))
    op.drop_column('orders', 'meals')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('meals', sa.VARCHAR(), nullable=True))
    op.drop_column('orders', 'dishs')
    # ### end Alembic commands ###
