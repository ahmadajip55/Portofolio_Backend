from blueprints import db
from flask_restful import fields
from sqlalchemy.sql.expression import text
from sqlalchemy import func
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Produks(db.Model):
    __tablename__="produks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_produk = db.Column(db.String(50), unique=True, nullable=False)
    seller = db.Column(db.String(50))
    harga = db.Column(db.Integer, nullable=False)
    stok = db.Column(db.Integer, nullable=False)
    kategori = db.Column(db.String(250), nullable=False)
    url_foto1 = db.Column(db.String(1000))
    url_foto2 = db.Column(db.String(1000))
    url_foto3 = db.Column(db.String(1000))
    deskripsi = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime(timezone=True), server_default = func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate = func.now())

    response_fields = {
        'id': fields.Integer,
        'nama_produk': fields.String,
        'seller': fields.String,
        'harga': fields.Integer,
        'stok': fields.Integer,
        'kategori': fields.String,
        'url_foto1': fields.String,
        'url_foto2': fields.String,
        'url_foto3': fields.String,
        'deskripsi': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, nama_produk, seller, harga, stok, kategori, url_foto1, url_foto2, url_foto3, deskripsi):
        self.nama_produk = nama_produk
        self.seller = seller
        self.harga = harga
        self.stok = stok
        self.kategori = kategori
        self.url_foto1 = url_foto1
        self.url_foto2 = url_foto2
        self.url_foto3 = url_foto3
        self.deskripsi = deskripsi

    def __repr__(self):
        return '<Produk %r>'% self.id