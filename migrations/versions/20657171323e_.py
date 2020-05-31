"""empty message

Revision ID: 20657171323e
Revises: 
Create Date: 2019-12-16 21:52:10.548298

"""
from alembic import op
import sqlalchemy as sa
from app.models.base import GUID
import uuid

# revision identifiers, used by Alembic.
revision = '20657171323e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('id', GUID(), default=uuid.uuid4, nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('users',
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('id', GUID(), default=uuid.uuid4, nullable=False),
                    sa.Column('username', sa.String(length=100), nullable=False),
                    sa.Column('email', sa.String(length=120), nullable=True),
                    sa.Column('fullname', sa.String(length=100), nullable=True),
                    sa.Column('password_hash', sa.String(length=255), nullable=True),
                    sa.Column('refer_id', GUID(), nullable=True),
                    sa.ForeignKeyConstraint(['refer_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('role')
    # ### end Alembic commands ###
