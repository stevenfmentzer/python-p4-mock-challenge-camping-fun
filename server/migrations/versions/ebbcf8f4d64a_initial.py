"""initial

Revision ID: ebbcf8f4d64a
Revises: 
Create Date: 2024-02-07 11:16:51.031946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebbcf8f4d64a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('difficulty', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_activities'))
    )
    op.create_table('campers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_campers'))
    )
    op.create_table('signups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('camper_id', sa.Integer(), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], name=op.f('fk_signups_activity_id_activities')),
    sa.ForeignKeyConstraint(['camper_id'], ['campers.id'], name=op.f('fk_signups_camper_id_campers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_signups'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('signups')
    op.drop_table('campers')
    op.drop_table('activities')
    # ### end Alembic commands ###
