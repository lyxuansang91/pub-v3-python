from app import models as m
from app.extensions import db


class AdvRepository(object):

    def find_by_email(self, email):
        return m.Adv.query.filter_by(email=email).first()

    def find_by_username(self, username):
        return m.Adv.query.filter_by(username=username).first()

    def find_by_id(self, adv_id):
        return m.Adv.query.get(adv_id)

    def update(self, adv_id, args):
        row_changed = m.Adv.filter(m.Adv.id == adv_id).update(args)
        db.session.commit()
        return row_changed == 1

    def delete(self, adv_id):
        row_changed = m.Adv.filter(m.Adv.id == adv_id).delete()
        db.session.commit()
        return row_changed == 1

    def create(self, args):
        adv = m.Adv(**args)
        db.session.add(adv)
        db.session.commit()
        return adv

    def get_list(self, args):
        return m.Adv.query.all()


adv_repo = AdvRepository()
