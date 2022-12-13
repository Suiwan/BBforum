"""empty message

Revision ID: 06d0ee2dc917
Revises: b9d05d9a35ef
Create Date: 2022-11-26 16:14:45.653378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06d0ee2dc917'
down_revision = 'b9d05d9a35ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('receiver_id', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_timestamp'), 'notification', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_notification_timestamp'), table_name='notification')
    op.drop_table('notification')
    # ### end Alembic commands ###