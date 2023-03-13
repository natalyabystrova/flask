"""realationships table

Revision ID: 140e04989ec7
Revises: 533d38f04a7f
Create Date: 2023-03-13 11:12:03.074593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '140e04989ec7'
down_revision = '533d38f04a7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_tag_association',
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], name=op.f('fk_article_tag_association_article_id_article')),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name=op.f('fk_article_tag_association_tag_id_tag'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article_tag_association')
    # ### end Alembic commands ###