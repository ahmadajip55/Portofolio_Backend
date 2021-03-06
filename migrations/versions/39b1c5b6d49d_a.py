"""a

Revision ID: 39b1c5b6d49d
Revises: 
Create Date: 2020-05-17 22:35:46.404204

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '39b1c5b6d49d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaksi', sa.Column('nama_produk', sa.String(length=1000), nullable=False))
    op.add_column('transaksi', sa.Column('username_pembeli', sa.String(length=1000), nullable=False))
    op.drop_column('transaksi', 'nama_produk5')
    op.drop_column('transaksi', 'nama_produk4')
    op.drop_column('transaksi', 'nama_produk1')
    op.drop_column('transaksi', 'nama_produk3')
    op.drop_column('transaksi', 'nama_produk2')
    op.drop_column('transaksi', 'catatan')
    op.drop_column('transaksi', 'pembeli')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaksi', sa.Column('pembeli', mysql.VARCHAR(length=1000), nullable=False))
    op.add_column('transaksi', sa.Column('catatan', mysql.VARCHAR(length=1000), nullable=True))
    op.add_column('transaksi', sa.Column('nama_produk2', mysql.VARCHAR(length=1000), nullable=True))
    op.add_column('transaksi', sa.Column('nama_produk3', mysql.VARCHAR(length=1000), nullable=True))
    op.add_column('transaksi', sa.Column('nama_produk1', mysql.VARCHAR(length=1000), nullable=False))
    op.add_column('transaksi', sa.Column('nama_produk4', mysql.VARCHAR(length=1000), nullable=True))
    op.add_column('transaksi', sa.Column('nama_produk5', mysql.VARCHAR(length=1000), nullable=True))
    op.drop_column('transaksi', 'username_pembeli')
    op.drop_column('transaksi', 'nama_produk')
    # ### end Alembic commands ###
