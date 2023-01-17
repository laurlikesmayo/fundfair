"""hello

Revision ID: f27776a90cc1
Revises: 6b637c8ce0a2
Create Date: 2023-01-05 16:26:02.570171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f27776a90cc1'
down_revision = '6b637c8ce0a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('poster_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['poster_id'], ['id'])
        batch_op.drop_column('author')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_added', sa.DateTime(), nullable=True))
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_column('date_added')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('poster_id')

    # ### end Alembic commands ###