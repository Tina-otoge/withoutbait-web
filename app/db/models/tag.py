import enum
import sqlalchemy as sa

from app import db


class Tag(db.Base, db.IdMixin, db.SlugMixin, db.TimedMixin):
    class Type(enum.Enum):
        """For special types of tags, do not use any type for "regular" tags"""
        WARN = enum.auto()

    name = sa.Column(sa.String)
    description = sa.Column(sa.String)
    score = sa.Column(sa.Integer, **db.default_value(0))
    type = sa.Column(sa.Enum(Type))
