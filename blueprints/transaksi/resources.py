import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints import pelapak_required, admin_required

from .model import Transaksis
from ..pembeli.model import Pembelis
from ..produk.model import Produks
from blueprints import pembeli_required

bp_transaksi = Blueprint('transaksi', __name__)
api = Api(bp_transaksi)

#CART
class TransaksiResource(Resource):
    @pembeli_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_produk', location='json', required=True)
        args = parser.parse_args()

        # Pembeli
        claims = get_jwt_claims()
        username_pembeli = claims['username']
        qry_pembeli = Pembelis.query.filter_by(username=username_pembeli).first()
        pembeli = marshal(qry_pembeli, Pembelis.response_fields)

        # nama_produk
        qry_produk= Produks.query.filter_by(nama_produk=args['nama_produk']).first()
        produk = marshal(qry_produk, Produks.response_fields)

        #transaksi
        qry_transaksi = Transaksis.query.filter_by(produk=args['nama_produk']).first()
        transaksi = marshal(qry_transaksi, Transaksis.response_fields)
        if qry_transaksi is None:
            total_harga = produk["harga"]
            total_barang = 1

            transaksi = Transaksis(username_pembeli, args['nama_produk'], total_harga, total_barang)
            
            db.session.add(transaksi)
            db.session.commit()

        else:
            db.session.delete(qry_transaksi)
            db.session.commit()
            total_barang = transaksi["total_barang"]
            total_barang = total_barang + 1
            total_harga = transaksi["total_harga"]
            total_harga = total_harga + produk["harga"]

            transaksi = Transaksis(username_pembeli, args['nama_produk'], total_harga, total_barang)

            db.session.add(transaksi)
            db.session.commit()
        
        transaksi = marshal(transaksi, Transaksis.response_fields)

        transaksi["produk"] = produk
        transaksi["pembeli"] = pembeli

        return transaksi, 200

    
    @pembeli_required
    def get(self):
        
        # Pembeli
        claims = get_jwt_claims()
        username_pembeli = claims['username']
        qry_pembeli = Pembelis.query.filter_by(username=username_pembeli).first()
        pembeli = marshal(qry_pembeli, Pembelis.response_fields)

        transaksi = Transaksis.query
        
        
        # rows = []
        # for row in transaksi.all():
        #     row = marshal(row, Transaksis.response_fields)
            
        #     qry_produk= Produks.query.filter_by(nama_produk=row["produk"]).all()
        #     produk = marshal(qry_produk, Produks.response_fields)
            
        #     row["pembeli"] = pembeli
        #     row["produk"] = produk
            
        #     rows.append(row)
        
        # return rows, 200

        return marshal(transaksi, Transaksis.response_fields), 200


    @pembeli_required
    def delete(self):
        
        transaksi = Transaksis.query

        for row in transaksi.all():
            db.session.delete(row)
            db.session.commit()

        return {"status": "Berhasil Memesan"}, 200

api.add_resource(TransaksiResource, '')