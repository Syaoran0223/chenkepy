"""empty message

Revision ID: 157af4e641e
Revises: 92af9d8e96
Create Date: 2017-03-07 19:46:49.322490

"""

# revision identifiers, used by Alembic.
revision = '157af4e641e'
down_revision = '92af9d8e96'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quest', sa.Column('order', sa.Integer(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quest', 'order')
    ### end Alembic commands ###
