from app import helper
from app import models as m
from app.extensions import db


class UserRepository(object):

    def find_by_id(self, user_id):
        return m.User.query.get(user_id)

    def find_by_username(self, username):
        return m.User.query.filter_by(username=username).first()

    def find_by_email(self, email):
        return m.User.query.filter_by(email=email).first()

    def create_user(self, args):
        user = m.User(**args)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user_id, args):
        m.User.query.filter(m.User.id == user_id).update(args)
        db.session.commit()

    def add_domain_to_user(self, user_id, url):
        domain = m.Domain(user_id=user_id, url=url)
        db.session.add(domain)
        db.session.commit()
        return domain

    def domains_from_user(self, user_id):
        return m.Domain.query.filter_by(user_id=user_id).all()

    def get_list_postback_logs(self, user_id, args):
        page = helper.get_page_from_args(args)
        per_page = helper.get_size_from_args(args)
        limit = (page - 1) * per_page
        count = m.PostbackLog.query.filter(m.PostbackLog.user_id == user_id).count()
        items = db.session.query(m.PostbackLog, m.Offer.name).join(m.Offer, m.PostbackLog.offer_id ==
                                                                   m.Offer.id).filter(m.PostbackLog.user_id == user_id).limit(per_page).offset(limit).all()
        return items, count, page, per_page


user_repo = UserRepository()
