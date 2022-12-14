"""empty message

Revision ID: 334afdcdc815
Revises: 
Create Date: 2022-10-22 11:29:51.198142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '334afdcdc815'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('text', sa.String(length=511), nullable=False),
    sa.Column('type_id', sa.String(length=200), nullable=False),
    sa.Column('author', sa.String(length=200), nullable=False),
    sa.Column('creat_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('img_url', sa.String(length=200), nullable=False),
    sa.Column('video_url', sa.String(length=200), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'author', 'img_url', 'video_url')
    )
    op.create_table('response',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(length=511), nullable=False),
    sa.Column('author', sa.String(length=255), nullable=False),
    sa.Column('creat_time', sa.DateTime(), nullable=True),
    sa.Column('img_url', sa.String(length=200), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'author', 'img_url')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('topic',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('theme', sa.String(length=200), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('type_id', sa.String(length=200), nullable=False),
    sa.Column('author', sa.String(length=200), nullable=False),
    sa.Column('creat_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'author')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=200), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('u_id', sa.Integer(), nullable=True),
    sa.Column('p_id', sa.Integer(), nullable=True),
    sa.Column('like_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['p_id'], ['post.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['u_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    op.drop_table('user')
    op.drop_table('topic')
    op.drop_table('role')
    op.drop_table('response')
    op.drop_table('post')
    # ### end Alembic commands ###
