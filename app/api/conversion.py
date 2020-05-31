import flask_restplus as fr
from flask_jwt_extended import (create_access_token, get_jwt_identity,  # noqa
                                jwt_optional, jwt_required)

from app.errors.exceptions import BadRequest, NotFound  # noqa
from app.repositories import user_repo, offer_repo, conversion_repo  # noqa

from ..utils.decorator import authorized, consumes, use_args  # noqa
from ..utils.crypto import base64_decodestring, base64_encodestring  # noqa
from ..utils.helper import get_model_value, send_request  # noqa


ns = fr.Namespace('conversions', description='Conversion related operations')


@ns.route('')
class APIConversionCreateAndList(fr.Resource):
    @use_args(**{
        'type': 'object',
        'properties': {
            'phone': {'type': 'string'},
            'name': {'type': 'string'},
            'address': {'type': 'string'},
            'publisher_code': {'type': 'string'},
            'offer_id': {'type': 'string'},
            'external_id': {'type': 'string'},
        },
        'required': ['phone', 'name', 'publisher_code', 'offer_id'],
    })
    def post(self, args):
        publisher_code = args.get('publisher_code')
        publisher_name = base64_decodestring(publisher_code)
        user = user_repo.find_by_username(publisher_name)
        if user is None:
            raise NotFound(code=404, message='User is not found')
        offer_alias = args.get('offer_id')
        offer = offer_repo.find_by_alias(offer_alias)
        if offer is None:
            raise NotFound(code=404, message='Offer is not found')
        args['offer_id'] = str(offer.id)
        args['publisher_name'] = publisher_name
        del args['publisher_code']
        conversion = conversion_repo.create(args)
        if conversion is None:
            raise BadRequest(message='Could not create conversion')
        try:
            if user.postback_url and user.postback_url != '':
                send_request(user, conversion)
        except Exception as err:
            print('err:', err)
            pass
        return {'item': conversion.to_model(), 'message': 'create conversion is successully'}, 201

    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'page': {'type': 'string'},
            'per_page': {'type': 'string'},
            'sort': {'type': 'string'},
            'filter': {'type': 'string'},
            'status': {'type': 'string'},
            'publisher_name': {'type': 'string'},
            'offer_alias': {'type': 'string'},
            'from_date': {'type': 'string'},
            'to_date': {'type': 'string'},
        }
    })
    def get(self, current_user, args):
        categories, count, page, per_page = conversion_repo.get_list(args)
        return {
            'items': [category.to_model() for category in categories],
            'count': count,
            'page': page,
            'per_page': per_page
        }, 200


@ns.route('/statistics')
class APIConversionStatistics(fr.Resource):

    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'from_date': {'type': 'string'},
            'to_date': {'type': 'string'},
            'alias': {'type': 'string'},
        },
        'required': ['from_date', 'to_date'],
    })
    def get(self, current_user, args):
        if 'alias' in args:
            offer = offer_repo.find_by_alias(args['alias'])
            args['offer_id'] = offer.id
        data = conversion_repo.get_statistic(args)
        return {'item': data}, 200


@ns.route('/statistics_by_date')
class APIConversionStatisticsByDate(fr.Resource):

    @jwt_required
    @authorized()
    def get(self, current_user):
        items = conversion_repo.get_statistic_by_date(current_user)
        data = []
        for item in items:
            count, status, date_created = item[0], item[1], item[2]
            data.append({'count': count, 'status': get_model_value(status), 'date_created': date_created.__str__()})

        return {'items': data}, 200
