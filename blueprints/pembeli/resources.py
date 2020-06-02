import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
import hashlib, uuid
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from .model import Pembelis
from blueprints import admin_required

bp_pembeli = Blueprint('pembeli', __name__)
api = Api(bp_pembeli)

class PembelisView(Resource):
    def get(self, id=None):
        qry = Pembelis.query.get(id)

        if qry is not None:
            return marshal(qry, Pembelis.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

# endpoint untuk delete pembeli
class PembelisDelete(Resource):   
    @admin_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('nama_pembeli', location='args', required=True)
        args = parser.parse_args()

        qry = Pembelis.query.filter_by(username=args['username']).filter_by(nama_pembeli=args['nama_pembeli']).first()
        
        claims = get_jwt_claims()
        status = claims['status']

        if status == "admin" :
            db.session.delete(qry)
            db.session.commit()
        else:
            return {'status': 'Anda bukan Admin'}, 404 
        
        return {"status": "Deleted"}, 200, {'Content-Type': 'application/json'}

# endpoint untuk register pembeli
class PembelisRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('email_pembeli', location='json', required=True)
        parser.add_argument('nama_pembeli', location='json', required=True)
        parser.add_argument('alamat_pembeli', location='json')
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        result = Pembelis(args['username'], hash_pass, args['email_pembeli'], args['nama_pembeli'], args['alamat_pembeli'], salt)

        db.session.add(result)
        db.session.commit()

        return marshal(result, Pembelis.response_fields), 200, {'Content-Type': 'application/json'}

        def options(self, id = None):
            return {}, 200

# endpoint untuk login pembeli
class PembelisLogin(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args')
        parser.add_argument('password', location='args')
        args = parser.parse_args()

        result = marshal(Pembelis.query.filter_by(username=args['username']).first(), Pembelis.response_fields)

        qry_pembeli = Pembelis.query.filter_by(username=args['username']).first()
        pembeli_salt = qry_pembeli.salt
        encode = hashlib.sha512(('%s%s' % (args['password'], pembeli_salt)).encode('utf-8')).hexdigest()
        
        if encode == qry_pembeli.password:
            qry_pembeli = marshal(qry_pembeli, Pembelis.jwt_claims_fields)
            qry_pembeli['status'] = "pembeli"
            token = create_access_token(identity=args['username'], user_claims=qry_pembeli)
            result['token'] = token
            return result, 200
        else:
            return {'status': 'UNAUTHORIZED', 'message':'invalid key or secret'}, 401

        def options(self, id = None):
            return {}, 200

api.add_resource(PembelisView, '', '/me/<id>')
api.add_resource(PembelisDelete, '', '/delete')
api.add_resource(PembelisRegister, '', '/register')
api.add_resource(PembelisLogin, '', '/login')