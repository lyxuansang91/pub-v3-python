import flask_restplus as fr
from flask_jwt_extended import (create_access_token, get_jwt_identity,  # noqa
                                jwt_optional, jwt_required)
from werkzeug.security import generate_password_hash

from app.errors.exceptions import BadRequest, NotFound  # noqa
from app.repositories import adv_repo  # noqa

from ..utils.decorator import authorized, consumes, use_args  # noqa

ns = fr.Namespace('advs', description='Advs related operations')


@ns.route('')
class APIAdvCreateAndList(fr.Resource):
    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'email': {'type': 'string', 'format': 'email'},
            'fullname': {'type': 'string'},
            'meta_data': {'type': 'object'},
        },
        'required': ['username', 'password'],
    })
    def post(self, current_user, args):
        username = args.get('username')
        if adv_repo.find_by_username(username) is not None:
            raise BadRequest(message='Adv is existed')
        if adv_repo.find_by_email(args.get('email')) is not None:
            raise BadRequest(message='Adv email is registered')
        adv = adv_repo.create(args)
        if adv is None:
            raise BadRequest(message='Could not created adv')
        return {'item': adv.to_model(), 'message': 'Create adv successfully'}, 201

    @jwt_required
    @authorized()
    def get(self, current_user, args):
        adv_repo.get_list(args)


@ns.route('/<string:adv_id>')
class APIAdvReadUpdateDelete(fr.Resource):
    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'password': {'type': 'string', 'maxLength': 20},
            'fullname': {'type': 'string'},
            'meta_data': {'type': 'object'},
        },
        'required': [],
    })
    def put(self, current_user, args, adv_id):
        if 'password' in args:
            args['password_hash'] = generate_password_hash(args['password'])
            del args['password']
        adv_repo.update(adv_id, args)
        return {}, 204

    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'password': {'type': 'string', 'maxLength': 20},
            'fullname': {'type': 'string'},
            'meta_data': {'type': 'object'},
        },
        'required': [],
    })
    def patch(self, current_user, args, adv_id):
        if 'password' in args:
            args['password_hash'] = generate_password_hash(args['password'])
            del args['password']
        adv_repo.update(adv_id, args)
        return {}, 204

    @jwt_required
    @authorized()
    def delete(self, current_user, adv_id):
        adv_repo.delete(adv_id)
        return {}, 204
