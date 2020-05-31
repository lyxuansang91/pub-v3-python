from uuid import uuid4

from app.extensions import db

from .base import GUID, BaseMixin, ModelHelper, ConversionStatus


class Conversion(db.Model, BaseMixin, ModelHelper):
    __tablename__ = 'conversions'
    __table_args__ = {'extend_existing': True}
    order_id = db.Column(db.Integer(), primary_key=True)
    id = db.Column(GUID(), default=uuid4)
    publisher_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(GUID(), db.ForeignKey('users.id'), nullable=True)
    publisher = db.relationship('User', foreign_keys=[user_id])
    phone = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    external_id = db.Column(db.String(100), unique=True, nullable=True)
    offer_id = db.Column(GUID(), db.ForeignKey('offers.id'))
    offer = db.relationship('Offer', foreign_keys=[offer_id])
    status = db.Column(db.Enum(ConversionStatus), default=lambda: ConversionStatus.PENDING)
