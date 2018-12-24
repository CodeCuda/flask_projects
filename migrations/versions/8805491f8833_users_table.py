"""users_table

Revision ID: 8805491f8833
Revises: 9d8351f12da2
Create Date: 2018-12-06 23:13:33.127897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8805491f8833'
down_revision = '9d8351f12da2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('photo_id', sa.String(length=128), nullable=True))



def downgrade():
    op.drop_column('user', 'photo_id')

