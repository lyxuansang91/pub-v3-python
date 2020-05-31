from app import models as m
from app.extensions import db
from app import helper


class OfferRespository(object):

    def find_by_id(self, id):
        return m.Offer.query.get(id)

    def update(self, id, args):
        row_changed = m.Offer.filter(m.Offer.id == id).update(args)
        db.session.commit()
        return row_changed == 1

    def delete(self, id):
        row_changed = m.Offer.filter(m.Offer.id == id).delete()
        db.session.commit()
        return row_changed == 1

    def create(self, args):
        offer = m.Offer.from_arguments(args)
        db.session.add(offer)
        db.session.commit()
        return offer

    def get_list(self, args):
        page = helper.get_page_from_args(args)
        per_page = helper.get_size_from_args(args)
        limit = (page - 1) * per_page
        base_query = m.Offer.query
        if 'category_id' in args:
            base_query = base_query.filter(m.Offer.category_id == args['category_id'])
        count = base_query.count()
        offers = base_query.limit(per_page).offset(limit).all()
        return offers, count

    def find_by_alias(self, alias):
        return m.Offer.query.filter(m.Offer.alias == alias).first()


offer_repo = OfferRespository()
