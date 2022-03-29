import sqlalchemy as sa

from app import db


class Game(db.Base, db.IdMixin, db.SlugMixin, db.TimedMixin):
    is_slug_from_igdb = sa.Column(sa.Boolean, **db.default_value(False))
    name = sa.Column(sa.String, nullable=False)
    subtitle = sa.Column(sa.String)
    official_url =  sa.Column(sa.String)
    cover_url = sa.Column(sa.String)
