"""parking_models_v1

Revision ID: 2a8c1be67b55
Revises: 0ec57ccb6aad
Create Date: 2023-01-27 01:16:45.058510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a8c1be67b55'
down_revision = '0ec57ccb6aad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=50), nullable=False),
    sa.Column('credit_card', sa.String(length=50), nullable=True),
    sa.Column('car_number', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('opened', sa.Boolean(), nullable=True),
    sa.Column('count_places', sa.Integer(), nullable=False),
    sa.Column('count_available_places', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client_parking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('parking_id', sa.Integer(), nullable=True),
    sa.Column('time_in', sa.DateTime(), nullable=True),
    sa.Column('time_out', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['parking_id'], ['parking.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking')
    )
    op.drop_table('products')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='products_pkey'),
    sa.UniqueConstraint('name', name='products_name_key')
    )
    op.drop_table('client_parking')
    op.drop_table('parking')
    op.drop_table('client')
    # ### end Alembic commands ###
