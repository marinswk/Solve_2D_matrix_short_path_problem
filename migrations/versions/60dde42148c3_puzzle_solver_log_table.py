"""Puzzle solver Log table

Revision ID: 60dde42148c3
Revises: 
Create Date: 2019-08-13 12:08:53.056675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60dde42148c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('puzzle_solver_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('n', sa.Integer(), nullable=False),
    sa.Column('grid', sa.String(), nullable=False),
    sa.Column('paths', sa.String(), nullable=True),
    sa.Column('error_flag', sa.Boolean(), nullable=False),
    sa.Column('request_time', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('puzzle_solver_log')
    # ### end Alembic commands ###
