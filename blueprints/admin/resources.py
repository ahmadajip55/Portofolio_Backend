import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
import hashlib, uuid
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from .model import Admins

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

# endpoint untuk register admin
class AdminsRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('kode_admin', location='json', required=True)
        args = parser.parse_args()

        if args['kode_admin'] == "AjayRockAdmin":
            salt = uuid.uuid4().hex
            encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()

            result = Admins(args['username'], hash_pass, salt)

            db.session.add(result)
            db.session.commit()

            return marshal(result, Admins.response_fields), 200, {'Content-Type': 'application/json'}
        else:
            return {'status': 'Maaf Anda bukan Admin'}, 200

# endpoint untuk login admin
class AdminsLogin(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args')
        parser.add_argument('password', location='args')
        parser.add_argument('kode_admin', location='args', required=True)
        args = parser.parse_args()

        if args['kode_admin'] == "AjayRockAdmin":
            result = marshal(Admins.query.filter_by(username=args['username']).first(), Admins.response_fields)

            qry_admin = Admins.query.filter_by(username=args['username']).first()
            admin_salt = qry_admin.salt
            encode = hashlib.sha512(('%s%s' % (args['password'], admin_salt)).encode('utf-8')).hexdigest()
            
            if encode == qry_admin.password:
                qry_admin = marshal(qry_admin, Admins.jwt_claims_fields)
                qry_admin['status'] = "Admin"
                token = create_access_token(identity=args['username'], user_claims=qry_admin)
                result['token'] = token
                return result, 200
            else:
                return {'status': 'UNAUTHORIZED', 'message':'invalid key or secret'}, 401
        else:
            return {'status': 'Maaf Anda bukan Admin'}, 200

api.add_resource(AdminsRegister, '', '/register')
api.add_resource(AdminsLogin, '', '/login')