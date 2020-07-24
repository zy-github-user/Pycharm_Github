"""empty message

Revision ID: 178f43fd1828
Revises: e013faa3ec04
Create Date: 2020-07-16 12:24:38.240016

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '178f43fd1828'
down_revision = 'e013faa3ec04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('article', 'type_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.create_foreign_key(None, 'article', 'article_type', ['type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.alter_column('article', 'type_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_table('article_type')
    # ### end Alembic commands ###
