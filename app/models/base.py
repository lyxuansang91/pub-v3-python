import enum
from datetime import datetime

from app.extensions import db
from app.utils.helper import get_model_value, get_model_value_primitive

from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class BaseMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)


class ModelHelper(object):
    def to_model(self):
        columns = list(map(lambda k: k.name, self.__table__.columns))
        excepts = [] if not hasattr(self, 'except_fields') else self.except_fields
        columns = [c for c in columns if c not in excepts]
        return {
            k: get_model_value(getattr(self, k)) for k in columns if hasattr(self, k)
        }

    def to_model_primitive(self):
        excepts = [] if not hasattr(self, 'except_fields') is None else self.except_fields
        columns = [column for column in map(lambda k: k.name, self.__table__.columns) if column not in excepts]
        return {
            k: get_model_value_primitive(getattr(self, k)) for k in columns if hasattr(self, k)
        }

    @classmethod
    def has_column(cls, column):
        columns = map(lambda k: k.name, cls.__table__.columns)
        return column in columns

    @classmethod
    def get_model(cls, args):
        return {
            k: args[k] for k in args if hasattr(cls, k)
        }

    @classmethod
    def get_model_put(cls, args):
        excepts = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']
        columns = map(lambda k: k, cls.__table__.columns)
        columns = [c for c in columns if c.name not in excepts]
        return {
            c.name: args.get(c.name) for c in columns if (c.name in args or c.nullable)
        }


class Enum(enum.Enum):
    @classmethod
    def includes(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def lists(cls):
        return list(map(lambda item: item.value, cls))


class ConversionStatus(Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    DUPLICATED = 'DUPLICATED'
    TRASHED = 'TRASHED'


class PostbackLogStatus(Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    FAILED = 'FAILED'
