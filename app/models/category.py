from uuid import uuid4

from app.extensions import db

from .base import GUID, BaseMixin, ModelHelper


class Category(db.Model, BaseMixin, ModelHelper):
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True}
    id = db.Column(GUID(), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
