# -*- coding: utf-8 -*-
import flask_restplus as fr
from flask_jwt_extended import (create_access_token, get_jwt_identity,  # noqa
                                jwt_optional, jwt_required)

from app.errors.exceptions import BadRequest, NotFound  # noqa
from app.repositories import category_repo  # noqa

from ..utils.decorator import authorized, consumes, use_args  # noqa

ns = fr.Namespace('categories', description='Category related operations')


@ns.route('')
class APICategoryCreateAndList(fr.Resource):
    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
        },
        'required': ['name'],
    })
    def post(self, current_user, args):
        category = category_repo.create(args)
        if category is None:
            raise BadRequest(message='Could not created category')
        return {'item': category.to_model(), 'message': 'Create category successfully'}, 201

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
        categories, count = category_repo.get_list(args)
        return {'items': [category.to_model() for category in categories], 'count': count}, 200


@ns.route('/<string:id>')
class APICategoryReadUpdateDelete(fr.Resource):

    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
        },
    })
    def put(self, current_user, args, id):
        return self._update(current_user, args, id)

    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
        },
    })
    def patch(self, current_user, args, id):
        return self._update(current_user, args, id)

    @jwt_required
    @authorized()
    def delete(self, current_user, id):
        category_repo.delete(id)
        return {}, 204

    def _update(self, current_user, args, id):
        category_repo.update(id, args)
        return {}, 204
