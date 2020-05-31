from uuid import uuid4
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db

from .base import GUID, BaseMixin, ModelHelper


class User(db.Model, BaseMixin, ModelHelper):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    except_fields = ['password_hash']
    id = db.Column(GUID(), primary_key=True, default=uuid4)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    fullname = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    refer_id = db.Column(GUID(), db.ForeignKey('users.id'), nullable=True)
    referer = db.relationship('User', remote_side=[id])
    postback_url = db.Column(db.String(255), nullable=True)

    @property
    def password(self):
        raise AttributeError('Password is not accessible')

    @password.setter
    def password(self, plaintext):
        self.password_hash = generate_password_hash(plaintext)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
