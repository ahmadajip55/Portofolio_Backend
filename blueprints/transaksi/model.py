from blueprints import db
from flask_restful import fields
from sqlalchemy.sql.expression import text
from sqlalchemy import func
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Transaksis(db.Model):
    __tablename__="transaksi"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pembeli = db.Column(db.String(1000), nullable=False)
    produk = db.Column(db.String(1000), nullable=False)
    total_harga = db.Column(db.Integer)
    total_barang = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default = func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate = func.now())

    response_fields = {
        'id': fields.Integer,
        'pembeli': fields.String,
        'produk': fields.String,
        'total_harga': fields.Integer,
        'total_barang': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, pembeli, produk, total_harga, total_barang):
        self.pembeli = pembeli
        self.produk = produk
        self.total_harga = total_harga
        self.total_barang = total_barang

    def __repr__(self):
        return '<Transaksi %r>'% self.id