from uuid import uuid4

from app.extensions import db

from .base import GUID, BaseMixin, ModelHelper, PostbackLogStatus


class PostbackLog(db.Model, BaseMixin, ModelHelper):
    __tablename__ = 'postback_logs'
    __table_args__ = {'extend_existing': True}

    id = db.Column(GUID(), primary_key=True, default=uuid4)
    user_id = db.Column(GUID(), db.ForeignKey('users.id'), nullable=True)
    order_id = db.Column(db.String(255), nullable=False)
    offer_id = db.Column(GUID, db.ForeignKey('offers.id'), nullable=True)
    url = db.Column(db.String(255), nullable=False)
    raw_url = db.Column(db.String(255), nullable=False)
    raw_response = db.Column(db.Text)
    status = db.Column(db.Enum(PostbackLogStatus), default=lambda: PostbackLogStatus.SUCCESS)
