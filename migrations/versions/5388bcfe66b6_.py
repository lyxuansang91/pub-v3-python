"""empty message

Revision ID: 5388bcfe66b6
Revises: bd5bb861b06b
Create Date: 2020-02-25 23:43:46.149981

"""
from alembic import op
import sqlalchemy as sa
from app.models.base import GUID
import uuid

# revision identifiers, used by Alembic.
revision = '5388bcfe66b6'
down_revision = 'bd5bb861b06b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('postback_logs',
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('id', GUID(), default=uuid.uuid4, nullable=False),
                    sa.Column('user_id', GUID(), default=uuid.uuid4, nullable=True),
                    sa.Column('order_id', sa.Integer(), nullable=True),
                    sa.Column('offer_id', GUID(), default=uuid.uuid4, nullable=True),
                    sa.Column('url', sa.String(length=255), nullable=False),
                    sa.Column('raw_url', sa.String(length=255), nullable=False),
                    sa.Column('raw_response', sa.Text(), nullable=True),
                    sa.Column('status', sa.Enum('SUCCESS', 'ERROR', 'FAILED', name='postbacklogstatus'), nullable=True),
                    sa.ForeignKeyConstraint(['offer_id'], ['offers.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('postback_logs')
    # ### end Alembic commands ###
