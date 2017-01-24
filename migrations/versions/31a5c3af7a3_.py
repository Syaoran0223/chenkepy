"""empty message

Revision ID: 31a5c3af7a3
Revises: 3ab8946f3af
Create Date: 2017-01-22 19:55:14.688053

"""

# revision identifiers, used by Alembic.
revision = '31a5c3af7a3'
down_revision = '3ab8946f3af'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exam', sa.Column('has_struct', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exam', 'has_struct')
    ### end Alembic commands ###
