from app import models as m
from app.extensions import db


class DomainRepository(object):

    def find_by_id(self, id):
        return m.Domain.query.get(id)

    def delete_by_id(self, id):
        row_changed = m.Domain.query.filter(m.Domain.id == id).delete()
        db.session.commit()
        return row_changed == 1

    def find_domain_by_url(self, url):
        return m.Domain.query.filter_by(url=url).first()


domain_repo = DomainRepository()
