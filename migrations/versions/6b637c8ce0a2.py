from alembic import op
import sqlalchemy as sa

revision = '6b637c8ce0a2'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('date_added', sa.DateTime),
    sa.Column('email', sa.String(50), unique=True, nullable = False),
    sa.Column('password',sa.String(50), nullable = False)
    )

    op.create_table('posts',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('title', sa.String(length=255)),
    sa.Column('content', sa.Text(1000)),
    sa.Column('author', sa.String(255)),
    sa.Column('slug', sa.String(255))
    )



def downgrade():
    op.drop_table('posts')
    op.drop_table('users')