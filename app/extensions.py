# -*- coding: utf-8 -*-
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restplus import Api
import flask_sqlalchemy as fsqla
from flask_jwt_extended import JWTManager
from flask import jsonify
from flask_cors import CORS


class SQLAlchemy(fsqla.SQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True


db = SQLAlchemy()
jwt_manager = JWTManager()
ma = Marshmallow()
migrate = Migrate(compare_type=True)
api = Api(version='1.0', title='Pub V3 API', description='Pub V3 API', doc='/docs')
cors = CORS()


@jwt_manager.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({'error': {'message': 'Invalid token', 'code': 401}}), 401


@jwt_manager.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({'error': {'message': 'Missing authorization header', 'code': 401}}), 401


@jwt_manager.expired_token_loader
def expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({'error': {'message': 'The {} token has expired'.format(token_type), 'code': 401}}), 401


@jwt_manager.user_claims_loader
def add_claims_to_access_token(identity):
    from app.repositories import user_repo
    user = user_repo.find_by_id(identity)
    if user:
        return {'fullname': user.fullname, 'email': user.email}
    else:
        return None
