"""empty message

Revision ID: 9eca104a0f50
Revises: 8632b9ef1592
Create Date: 2023-05-10 22:51:56.197511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9eca104a0f50'
down_revision = '8632b9ef1592'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('url', schema=None) as batch_op:
        batch_op.alter_column('short_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('short_code',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('url', schema=None) as batch_op:
        batch_op.alter_column('short_code',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('short_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)

    # ### end Alembic commands ###
