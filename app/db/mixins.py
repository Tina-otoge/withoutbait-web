from datetime import datetime
import re
import sqlalchemy as sa
from sqlalchemy import orm


@orm.declarative_mixin
class IdMixin:
    id = sa.Column(sa.Integer, primary_key=True)

@orm.declarative_mixin
class SlugMixin:
    slug = sa.Column(sa.String, unique=True)

    @staticmethod
    def slugify(s: str):
        return re.sub(r'\W', '-', s.lower())

@orm.declarative_mixin
class CreatedMixin:
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)


@orm.declarative_mixin
class TimedMixin(CreatedMixin):
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow)
