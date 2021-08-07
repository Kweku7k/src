"""empty message

Revision ID: 26440417d953
Revises: 7b3b846f1344
Create Date: 2021-08-06 11:20:41.139109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26440417d953'
down_revision = '7b3b846f1344'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidateId', sa.String(), nullable=False),
    sa.Column('amount', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
