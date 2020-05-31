from uuid import uuid4

from app.extensions import db

from .base import GUID, BaseMixin, ModelHelper


class Domain(db.Model, BaseMixin, ModelHelper):
    __tablename__ = 'domains'
    __table_args__ = {'extend_existing': True}
    id = db.Column(GUID(), primary_key=True, default=uuid4)
    user_id = db.Column(GUID(), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    url = db.Column(db.String(100), unique=True, nullable=False)
