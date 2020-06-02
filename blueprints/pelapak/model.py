from blueprints import db
from flask_restful import fields
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Pelapaks(db.Model):
    __tablename__="pelapaks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    nama_pelapak = db.Column(db.String(250), nullable=False)
    alamat_pelapak = db.Column(db.String(250))
    salt = db.Column(db.String(250))

    response_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'nama_pelapak': fields.String,
        'alamat_pelapak': fields.String
    }

    jwt_claims_fields ={
        'id': fields.Integer,
        'username': fields.String,
        'nama_pelapak': fields.String
    }

    def __init__(self, username, password, nama_pelapak, alamat_pelapak, salt):
        self.username = username
        self.password = password
        self.nama_pelapak = nama_pelapak
        self.alamat_pelapak = alamat_pelapak
        self.salt = salt

    def __repr__(self):
        return '<Pelapak %r>'% self.id