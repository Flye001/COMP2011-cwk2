"""Store password

Revision ID: 1cd31c49fd78
Revises: d576b49187ad
Create Date: 2024-11-26 11:34:55.038539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cd31c49fd78'
down_revision = 'd576b49187ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=100), nullable=False))
        batch_op.alter_column('fname',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('lname',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('account_type',
               existing_type=sa.VARCHAR(length=7),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('account_type',
               existing_type=sa.VARCHAR(length=7),
               nullable=True)
        batch_op.alter_column('lname',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('fname',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###