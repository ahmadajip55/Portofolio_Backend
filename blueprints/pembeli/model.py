from blueprints import db
from flask_restful import fields
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Pembelis(db.Model):
    __tablename__="pembelis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email_pembeli = db.Column(db.String(250), nullable=False)
    nama_pembeli = db.Column(db.String(250), nullable=False)
    alamat_pembeli = db.Column(db.String(250))
    salt = db.Column(db.String(250))

    response_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'email_pembeli': fields.String,
        'nama_pembeli': fields.String,
        'alamat_pembeli': fields.String
    }

    jwt_claims_fields ={
        'id': fields.Integer,
        'username': fields.String,
        'nama_pembeli': fields.String
    }

    def __init__(self, username, password, email_pembeli, nama_pembeli, alamat_pembeli, salt):
        self.username = username
        self.password = password
        self.email_pembeli = email_pembeli
        self.nama_pembeli = nama_pembeli
        self.alamat_pembeli = alamat_pembeli
        self.salt = salt

    def __repr__(self):
        return '<Pembeli %r>'% self.id