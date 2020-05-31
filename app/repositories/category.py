from app import models as m
from app.extensions import db
from app import helper


class CategoryRepository(object):

    def find_by_id(self, id):
        return m.Category.query.get(id)

    def update(self, id, args):
        row_changed = m.Category.filter(m.Category.id == id).update(args)
        db.session.commit()
        return row_changed == 1

    def delete(self, id):
        row_changed = m.Category.filter(m.Category.id == id).delete()
        db.session.commit()
        return row_changed == 1

    def create(self, args):
        category = m.Category(**args)
        db.session.add(category)
        db.session.commit()
        return category

    def get_list(self, args):
        page = helper.get_page_from_args(args)
        per_page = helper.get_size_from_args(args)
        limit = (page - 1) * per_page
        count = m.Category.query.count()
        categories = m.Category.query.limit(per_page).offset(limit).all()
        return categories, count


category_repo = CategoryRepository()
