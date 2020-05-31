import flask_restplus as fr
from flask_jwt_extended import (create_access_token, get_jwt_identity,  # noqa
                                jwt_optional, jwt_required)

from app.errors.exceptions import BadRequest, NotFound  # noqa
from app.repositories import offer_repo  # noqa

from ..utils.decorator import authorized, consumes, use_args  # noqa

ns = fr.Namespace('offers', description='Offer related operations')


@ns.route('')
class APIOfferCreateAndList(fr.Resource):
    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'alias': {'type': 'string'},
            'description': {'type': 'string'},
            'short_desc': {'type': 'string'},
            'geo': {'type': 'string'},
            'name': {'type': 'string'},
            'img': {'type': 'string', 'format': 'uri'},
            'category_id': {'type': 'string', 'format': 'uuid'},
            'country_code': {'type': 'integer'},
            'payout_share': {'type': 'number'},
            'ecpc': {'type': 'number'},
            'price': {'type': 'number'},
            'adv_id': {'type': 'string', 'format': 'uuid'},
            'aff_sub_pub': {'type': 'string'},
            'aff_sub_order': {'type': 'string'},
            'aff_click_id': {'type': 'string'},
            'aff_pub_sub2': {'type': 'string'},
            'account_name':  {'type': 'string'},
        },
        'required': ['name', 'alias', 'description', 'category_id', 'adv_id', 'price', 'img'],
    })
    def post(self, current_user, args):
        offer = offer_repo.create(args)
        if offer is None:
            raise BadRequest(message='Could not create offer')
        return {'item': offer.to_model(), 'message': 'Create offer successfully'}, 201

    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'page': {'type': 'string'},
            'per_page': {'type': 'string'},
            'sort': {'type': 'string'},
            'filter': {'type': 'string'},
            'category_id': {'type': 'string'},
        }
    })
    def get(self, current_user, args):
        offers, count = offer_repo.get_list(args)
        return {'items': [offer.to_model() for offer in offers], 'count': count}, 200


@ns.route('/<string:id>')
class APIOfferReadUpdateDelete(fr.Resource):

    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'description': {'type': 'string'},
            'short_desc': {'type': 'string'},
            'geo': {'type': 'string'},
            'name': {'type': 'string'},
            'img': {'type': 'string', 'format': 'uri'},
            'category_id': {'type': 'string', 'format': 'uuid'},
            'country_code': {'type': 'integer'},
            'payout_share': {'type': 'number'},
            'ecpc': {'type': 'number'},
            'price': {'type': 'number'},
            'adv_id': {'type': 'string', 'format': 'uuid'},
            'aff_sub_pub': {'type': 'string'},
            'aff_sub_order': {'type': 'string'},
            'aff_click_id': {'type': 'string'},
            'aff_pub_sub2': {'type': 'string'},
            'account_name':  {'type': 'string'},
            'active': {'type': 'boolean'},
        },
    })
    def put(self, current_user, args, id):
        return self._update(current_user, args, id)

    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'description': {'type': 'string'},
            'short_desc': {'type': 'string'},
            'geo': {'type': 'string'},
            'name': {'type': 'string'},
            'img': {'type': 'string', 'format': 'uri'},
            'category_id': {'type': 'string', 'format': 'uuid'},
            'country_code': {'type': 'integer'},
            'payout_share': {'type': 'number'},
            'ecpc': {'type': 'number'},
            'price': {'type': 'number'},
            'adv_id': {'type': 'string', 'format': 'uuid'},
            'aff_sub_pub': {'type': 'string'},
            'aff_sub_order': {'type': 'string'},
            'aff_click_id': {'type': 'string'},
            'aff_pub_sub2': {'type': 'string'},
            'account_name':  {'type': 'string'},
            'active': {'type': 'boolean'},
        },
    })
    def patch(self, current_user, args, id):
        return self._update(current_user, args, id)

    @jwt_required
    @authorized()
    def delete(self, current_user, id):
        offer_repo.delete(id)
        return {}, 204

    def _update(self, current_user, args, id):
        aff_sub_pub = args.get('aff_sub_pub')
        aff_sub_order = args.get('aff_sub_order')
        aff_click_id = args.get('aff_click_id')
        aff_pub_sub2 = args.get('aff_pub_sub2')
        account_name = args.get('account_name')
        args['meta_data'] = {'aff_sub_pub': aff_sub_pub, 'aff_sub_order': aff_sub_order,
                             'aff_click_id': aff_click_id, 'aff_pub_sub2': aff_pub_sub2, 'account_name': account_name}
        del args['aff_sub_pub']
        del args['aff_sub_order']
        del args['aff_click_id']
        del args['aff_pub_sub_2']
        del args['account_name']
        offer_repo.update(id, args)
        return {}, 204
