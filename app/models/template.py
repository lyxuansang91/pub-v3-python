from uuid import uuid4

from app.extensions import db
from .base import GUID, BaseMixin, ModelHelper


class Template(db.Model, ModelHelper, BaseMixin):
    __tablename__ = 'templates'
    __table_args__ = {'extend_existing': True}
    id = db.Column(GUID(), primary_key=True, default=uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
