"""empty message

Revision ID: 9519ddb43615
Revises: f5c3508767b9
Create Date: 2019-09-23 12:44:20.762915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9519ddb43615'
down_revision = 'f5c3508767b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_article_likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['blog_article.id'], name=op.f('fk_blog_article_likes_article_id_blog_article')),
    sa.ForeignKeyConstraint(['user_id'], ['blog_user.id'], name=op.f('fk_blog_article_likes_user_id_blog_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_blog_article_likes'))
    )
    op.create_table('blog_article_tag',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['blog_article.id'], name=op.f('fk_blog_article_tag_article_id_blog_article')),
    sa.ForeignKeyConstraint(['tag_id'], ['blog_tag.id'], name=op.f('fk_blog_article_tag_tag_id_blog_tag'))
    )
    op.create_table('likes_in_article',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['blog_article.id'], name=op.f('fk_likes_in_article_article_id_blog_article')),
    sa.ForeignKeyConstraint(['user_id'], ['blog_user.id'], name=op.f('fk_likes_in_article_user_id_blog_user'))
    )
    op.create_table('tags_in_article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['blog_article.id'], name=op.f('fk_tags_in_article_article_id_blog_article')),
    sa.ForeignKeyConstraint(['tag_id'], ['blog_tag.id'], name=op.f('fk_tags_in_article_tag_id_blog_tag')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tags_in_article'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags_in_article')
    op.drop_table('likes_in_article')
    op.drop_table('blog_article_tag')
    op.drop_table('blog_article_likes')
    # ### end Alembic commands ###
