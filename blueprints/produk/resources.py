import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints import pelapak_required, admin_required

from .model import Produks
from ..pelapak.model import Pelapaks

bp_produk = Blueprint('product', __name__)
api = Api(bp_produk)

class ProduksResource(Resource):
    def get(self, id=None):
        qry = Produks.query.get(id)

        produk = marshal(qry, Produks.response_fields)

        pelapak = marshal(Pelapaks.query.filter_by(username=produk["seller"]).all(), Pelapaks.response_fields)

        produk["seller"] = pelapak

        if qry is not None:
            return produk, 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

class ProdukPost(Resource):
    @pelapak_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_produk', location='json', required=True)
        parser.add_argument('harga', location='json', required=True)
        parser.add_argument('stok', location='json', required=True)
        parser.add_argument('kategori', location='json', required=True, help='invalid status', choices=('batusedimen', 'mineralbijih', 'fosil', 'batubeku', 'batumetamorf', 'batualterasi'))
        parser.add_argument('url_foto1', location='json')
        parser.add_argument('url_foto2', location='json')
        parser.add_argument('url_foto3', location='json')
        parser.add_argument('deskripsi', location='json')
        args = parser.parse_args()

        claims = get_jwt_claims()
        seller = claims['username']

        produks = Produks(args['nama_produk'], seller, args['harga'], args['stok'], args['kategori'], args['url_foto1'], args['url_foto2'], args['url_foto3'], args['deskripsi'])
        
        db.session.add(produks)
        db.session.commit()
        
        qry = Pelapaks.query.filter_by(username=seller).all()
        pelapak = marshal(qry, Pelapaks.response_fields)
        
        print_produks = marshal(produks, Produks.response_fields)
        print_produks['seller'] = pelapak[0]

        app.logger.debug('DEBUG : %s', produks)
        return print_produks, 200, {'Content-Type': 'application/json'}

    @pelapak_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_produk', location='json', required=True)
        parser.add_argument('harga', location='json', required=True)
        parser.add_argument('stok', location='json', required=True)
        parser.add_argument('kategori', location='json', required=True, help='invalid status', choices=('batusedimen', 'mineralbijih', 'fosil', 'batubeku', 'batumetamorf', 'batualterasi'))
        parser.add_argument('url_foto1', location='json')
        parser.add_argument('url_foto2', location='json')
        parser.add_argument('url_foto3', location='json')
        parser.add_argument('deskripsi', location='json')
        args = parser.parse_args()

        produks = Produks.query.filter_by(nama_produk=args['nama_produk']).first()
        
        claims = get_jwt_claims()
        seller = claims['username']

        if seller == produks.seller :
            produks.harga = args['harga']
            produks.stok = args['stok']
            produks.kategori = args['kategori']
            produks.url_foto1 = args['url_foto1']
            produks.url_foto2 = args['url_foto2']
            produks.url_foto3 = args['url_foto3']
            produks.deskripsi = args['deskripsi']
            db.session.commit()
        elif qry is none:
            return {'status': 'Not_Found'}, 404
        else:
            return {'status': 'Produk bukan milik Pelapak'}, 404 
        
        qry = Pelapaks.query.filter_by(username=seller).all()
        pelapak = marshal(qry, Pelapaks.response_fields)
        
        print_produks = marshal(produks, Produks.response_fields)
        print_produks['seller'] = pelapak[0]

        return print_produks, 200, {'Content-Type': 'application/json'}

    @pelapak_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_produk', location='args', required=True)
        args = parser.parse_args()

        qry = Produks.query.filter_by(nama_produk=args['nama_produk']).first()
        
        claims = get_jwt_claims()
        seller = claims['username']

        if seller == qry.seller:
            db.session.delete(qry)
            db.session.commit()
        else:
            return {'status': 'Produk bukan milik Pelapak'}, 404 
        
        return {"status": "Deleted"}, 200, {'Content-Type': 'application/json'}

class ProdukSearch(Resource):
    # search by kategori
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('kategori', location='args', default='None')
        args = parser.parse_args()

        qry = Produks.query.filter_by(kategori=args['kategori']).all()
        produk = marshal(qry, Produks.response_fields)

        rows = []
        for row in produk:
            qry = Pelapaks.query.filter_by(username=row['seller']).all()
            pelapak = marshal(qry, Pelapaks.response_fields)
            row['seller'] = pelapak
            rows.append(row)

        if qry:
            return rows, 200
        else:
            return {'status': 'NOT FOUND'}, 404


class ProduksList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=(
            'seller',
            'harga',
            'stok'
        ))
        parser.add_argument('sort', location='args', help='invalid status', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Produks.query

        if args['orderby'] is not None:
            if args['orderby'] == 'seller':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Produks.seller))
                else:
                    qry = qry.order_by(Produks.seller)
            elif args['orderby'] == 'harga':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Produks.harga))
                else:
                    qry = qry.order_by(Produks.harga)
            elif args['orderby'] == 'stok':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Produks.stok))
                else:
                    qry = qry.order_by(Produks.stok)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            row = marshal(row, Produks.response_fields)
            qry = Pelapaks.query.filter_by(username=row['seller']).all()
            pelapak = marshal(qry, Pelapaks.response_fields)
            row['seller'] = pelapak
            rows.append(row)

        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(ProduksList, '', '/list')
api.add_resource(ProduksResource, '', '/<id>')
api.add_resource(ProdukPost, '', '/edit')
api.add_resource(ProdukSearch, '', '/kategori')