# -*- coding: utf-8 -*-
import flask_restplus as fr
from flask_jwt_extended import (create_access_token, get_jwt_identity,  # noqa
                                jwt_optional, jwt_required)

from app.errors.exceptions import BadRequest, NotFound  # noqa
from app.repositories import user_repo, domain_repo

from ..utils.decorator import authorized, consumes, use_args  # noqa

ns = fr.Namespace('domains', description='Domains related operations')


@ns.route('')
class APIUserAddDomainAndList(fr.Resource):
    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'url': {
                'type': 'string',
            },
        },
        'required': ['url'],
    })
    def post(self, current_user, args):
        url = args.get('url')
        domain = domain_repo.find_domain_by_url(url)
        if domain is not None:
            raise BadRequest(message='Domain is existed')

        domain = user_repo.add_domain_to_user(current_user.id, url)
        if domain is None:
            raise BadRequest(message='Could not create domain')
        return {'item': domain.to_model(), 'message': 'create domain is successfully'}, 201

    @jwt_required
    @authorized()
    def get(self, current_user):
        domains = user_repo.domains_from_user(current_user.id)
        return {'items': [domain.to_model() for domain in domains]}, 200


@ns.route('/<string:id>')
class APIDomainDelele(fr.Resource):
    @jwt_required
    @authorized()
    def delete(self, current_user, id):
        domain = domain_repo.find_by_id(id)
        if domain and str(domain.user_id) == str(current_user.id):
            domain_repo.delete_by_id(id)
        return {}, 204
