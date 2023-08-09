"""ADDED IMAGE ATTRIBUTES

Revision ID: 16758856b097
Revises: bc7d3fd5238c
Create Date: 2023-08-09 10:23:06.208334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16758856b097'
down_revision = 'bc7d3fd5238c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('superadmin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('superadmin_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))
        batch_op.drop_column('superadmin_id_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('superadmin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('superadmin_id_id', sa.INTEGER(), autoincrement=True, nullable=False))
        batch_op.drop_column('image')
        batch_op.drop_column('superadmin_id')

    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###