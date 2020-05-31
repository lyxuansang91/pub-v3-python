import flask_restplus as fr
from flask_jwt_extended import (create_access_token, get_jwt_identity,  # noqa
                                jwt_optional, jwt_required)

from app.errors.exceptions import BadRequest, NotFound
from app.repositories import user_repo

from ..utils.decorator import authorized, consumes, use_args

ns = fr.Namespace('users', description='Users related operations')


@ns.route('/profile')
class APIUserProfile(fr.Resource):
    @jwt_required
    @authorized()
    def get(self, current_user):
        return {'item': current_user.to_model(), 'message': 'Get UserInfo Successfully'}, 200

    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'postback_url': {'type': 'string'},
        }
    })
    def patch(self, current_user, args):
        user_repo.update_user(current_user.id, args)
        return {'item': current_user.to_model(), 'message': 'Update UserInfo successfully'}, 204


@ns.route('/profile/postback_logs')
class APIUserPostbackLogs(fr.Resource):
    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'page': {'type': 'string'},
            'per_page': {'type': 'string'},
            'sort': {'type': 'string'},
            'filter': {'type': 'string'},
        }
    })
    def get(self, current_user, args):
        items, count, page, per_page = user_repo.get_list_postback_logs(current_user.id, args)
        return {
            'items': [{'offer_name': offer_name, **postback_log.to_model()} for postback_log, offer_name in items],
            'count': count,
            'page': page,
            'per_page': per_page
        }, 200


@ns.route('/login')
class APIUserLogin(fr.Resource):
    @consumes('application/json')
    @use_args(**{
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
        },
        'required': ['username', 'password'],
    })
    def post(self, args):
        username = args.get('username')
        if username is None or username == '':
            raise BadRequest(message='Username is required')
        user = user_repo.find_by_username(username)
        if user is None:
            raise NotFound(message='User is not found')
        password = args.get('password')
        if not user.check_password(password):
            raise BadRequest(message='Wrong username or password')
        access_token = create_access_token(user.id)
        return {'item': {'accessToken': access_token}, 'message': 'Login successully'}, 200


@ns.route('/register')
class APIUserRegister(fr.Resource):
    @consumes('application/json')
    @use_args(**{
        'type': 'object',
        'properties': {
            'email': {
                'type': 'string',
                'format': 'email'
            },
            'username': {'type': 'string', 'maxLength': 128},
            'password': {'type': 'string'},
            'fullname': {'type': 'string', 'maxLength': 128},
            'referrer': {'type': 'string', 'maxLength': 128},
        },
        'required': ['username', 'password'],
    })
    def post(self, args):
        username = args.get('username')
        email = args.get('email')
        if user_repo.find_by_username(username) is not None:
            raise BadRequest(message='User is existed')
        if user_repo.find_by_email(email) is not None:
            raise BadRequest(message='Email is registered')
        if 'referrer' in args:
            refer = user_repo.find_by_username(args.get('referrer'))
            if refer is None:
                raise BadRequest(message='Referrer is not found')
            args['refer_id'] = refer.id
            del args['referrer']
        user = user_repo.create_user(args)
        if user is None:
            raise BadRequest(message='Could not create user')
        return {'item': user.to_model(), 'message': 'create User is successfully'}, 200
