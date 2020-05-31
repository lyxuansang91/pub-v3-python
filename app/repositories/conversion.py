from app import helper
from app import models as m
from app.extensions import db
from datetime import date, timedelta


class ConversionRepository(object):

    def find_by_id(self, id):
        return m.Conversion.query.get(id)

    def update(self, id, args):
        row_changed = m.Conversion.filter(m.Conversion.id == id).update(args)
        db.session.commit()
        return row_changed == 1

    def delete(self, id):
        row_changed = m.Conversion.filter(m.Conversion.id == id).delete()
        db.session.commit()
        return row_changed == 1

    def create(self, args):
        try:
            conversion = m.Conversion(**args)
            db.session.add(conversion)
            db.session.commit()
            return conversion
        except Exception as e:
            print(e)
            return None

    def get_list(self, args):
        """
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
        """
        page = helper.get_page_from_args(args)
        per_page = helper.get_size_from_args(args)
        limit = (page - 1) * per_page
        base_query = m.Conversion.query.filter(m.Conversion.active)
        if 'publisher_name' in args:
            publisher_name = args.get('publisher_name')
            base_query = base_query.filter(m.Conversion.publisher_name == publisher_name)
        if 'status' in args:
            status = args.get('status')
            base_query = base_query.filter(m.Conversion.status == status)
        if 'offer_alias' in args:
            alias = args.get('offer_alias')
            offer = m.Offer.query.filter(m.Offer.alias == alias).first()
            base_query = base_query.filter(m.Conversion.offer_id == offer.id)
        if 'from_date' in args and 'to_date' in args:
            from sqlalchemy import and_, func
            from_date = helper.datetime_from_timestamp(int(args.get('from_date'))).strftime('%Y-%m-%d')
            to_date = helper.datetime_from_timestamp(int(args.get('to_date'))).strftime('%Y-%m-%d')
            base_query = base_query.filter(and_(func.date(m.Conversion.created_at) <= to_date,
                                                func.date(m.Conversion.created_at) >= from_date))
        count = 1
        conversions = base_query.limit(per_page).offset(limit).all()
        return conversions, count, page, per_page

    def get_statistic(self, args):
        """ Get statistics
        'type': 'object',
        'properties': {
            'from_date': {'type': 'string'},
            'to_date': {'type': 'string'},
            'alias': {'type': 'string'},
            'offer_id: {'type': 'string'},
        },
        'required': ['from_date', 'to_date'],
        """
        from sqlalchemy import and_, func
        from_date = helper.datetime_from_timestamp(int(args.get('from_date'))).strftime('%Y-%m-%d')
        to_date = helper.datetime_from_timestamp(int(args.get('to_date'))).strftime('%Y-%m-%d')
        base_query = m.Conversion.query.filter(and_(func.date(m.Conversion.created_at) <= to_date,
                                                    func.date(m.Conversion.created_at) >= from_date))
        if 'offer_id' in args:
            base_query = base_query.filter(m.Conversion.offer_id == args['offer_id'])
        base_query = base_query.order_by(m.Conversion.status)
        all_conversions = base_query.all()
        # GET status PENDING
        pending_conversions = list(filter(lambda conversion: conversion.status == m.ConversionStatus.PENDING, all_conversions))
        approved_conversions = list(filter(lambda conversion: conversion.status == m.ConversionStatus.APPROVED, all_conversions))
        rejected_conversions = list(filter(lambda conversion: conversion.status == m.ConversionStatus.REJECTED, all_conversions))
        duplicated_conversions = list(filter(lambda conversion: conversion.status == m.ConversionStatus.DUPLICATED, all_conversions))
        trashed_conversions = list(filter(lambda conversion: conversion.status == m.ConversionStatus.TRASHED, all_conversions))
        approved_rate = 0 if len(all_conversions) == 0 else len(approved_conversions) / (len(all_conversions) - len(trashed_conversions))
        return {
            'total': len(all_conversions),
            'pending': len(pending_conversions),
            'approved': len(approved_conversions),
            'rejected': len(rejected_conversions),
            'trashed': len(trashed_conversions),
            'duplicated': len(duplicated_conversions),
            'approved_rate': approved_rate * 100,
        }

    def get_statistic_by_date(self, current_user):
        today = date.today()
        ten_previous_day = today - timedelta(days=10)

        from sqlalchemy import and_, func  # noqa
        data = db.session.query(
            func.count(m.Conversion.status), m.Conversion.status, func.date(m.Conversion.created_at)
        ).filter(and_(
            m.Conversion.publisher_name == current_user.username,
            m.Conversion.created_at >= ten_previous_day,
            m.Conversion.created_at <= today)).group_by(m.Conversion.status, func.date(m.Conversion.created_at)).order_by(func.date(m.Conversion.created_at)).all()
        return data


conversion_repo = ConversionRepository()
