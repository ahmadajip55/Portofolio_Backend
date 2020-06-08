import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
import hashlib, uuid
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from .model import Pelapaks
from blueprints import admin_required

bp_pelapak = Blueprint('pelapak', __name__)
api = Api(bp_pelapak)

class PelapaksView(Resource):
    def get(self, id=None):
        qry = Pelapaks.query.get(id)

        if qry is not None:
            return marshal(qry, Pelapaks.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

class PelapaksDelete(Resource):   
    @admin_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('nama_pelapak', location='args', required=True)
        args = parser.parse_args()

        qry = Pelapaks.query.filter_by(username=args['username']).filter_by(nama_pelapak=args['nama_pelapak']).first()
        
        claims = get_jwt_claims()
        status = claims['status']

        if status == "admin" :
            db.session.delete(qry)
            db.session.commit()
        else:
            return {'status': 'Anda bukan Admin'}, 404 
        
        return {"status": "Deleted"}, 200, {'Content-Type': 'application/json'}

# endpoint untuk register pelapak
class PelapaksRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('nama_pelapak', location='json', required=True)
        parser.add_argument('alamat_pelapak', location='json')
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        result = Pelapaks(args['username'], hash_pass, args['nama_pelapak'], args['alamat_pelapak'], salt)

        db.session.add(result)
        db.session.commit()

        return marshal(result, Pelapaks.response_fields), 200, {'Content-Type': 'application/json'}

    def get(self):
        return {"name": "ajay", "status": "coba"} 200

# endpoint untuk login pelapak
class PelapaksLogin(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args')
        parser.add_argument('password', location='args')
        args = parser.parse_args()

        result = marshal(Pelapaks.query.filter_by(username=args['username']).first(), Pelapaks.response_fields)

        qry_pelapak = Pelapaks.query.filter_by(username=args['username']).first()
        pelapak_salt = qry_pelapak.salt
        encode = hashlib.sha512(('%s%s' % (args['password'], pelapak_salt)).encode('utf-8')).hexdigest()
        
        if encode == qry_pelapak.password:
            qry_pelapak = marshal(qry_pelapak, Pelapaks.jwt_claims_fields)
            qry_pelapak['status'] = "pelapak"
            token = create_access_token(identity=args['username'], user_claims=qry_pelapak)
            result['token'] = token
            return result, 200
        else:
            return {'status': 'UNAUTHORIZED', 'message':'invalid key or secret'}, 401


api.add_resource(PelapaksView, '', '/me/<id>')
api.add_resource(PelapaksDelete, '', '/delete')
api.add_resource(PelapaksRegister, '', '/register')
api.add_resource(PelapaksLogin, '', '/login')