import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Game(db.Base, db.IdMixin, db.SlugMixin, db.TimedMixin):
    REPR_KEYS = {'name'}

    is_slug_from_igdb = sa.Column(sa.Boolean, **db.default_value(False))
    name = sa.Column(sa.String, nullable=False)
    subtitle = sa.Column(sa.String)
    official_url =  sa.Column(sa.String)
    cover_url = sa.Column(sa.String)
    score = sa.Column(sa.Integer)
    views = sa.Column(sa.Integer, **db.default_value(0))
    igdb_score = sa.Column(sa.Float)
    summary = sa.Column(sa.String)
    release_date = sa.Column(sa.DateTime)

    tags = orm.relationship('Tag', secondary='game_tags', backref='games')
    genres = orm.relationship('Genre', secondary='game_genres', backref='games')
    platforms = orm.relationship('Platform', secondary='game_platforms', backref='games', lazy='dynamic')
    reviews = orm.relationship('Review', order_by='Review.id.desc()')

    @property
    def rating(self):
        if not self.score:
            return 'Not rated'
        if self.score >= 75:
            return 'good'
        if self.score >= 35:
            return 'meh'
        return 'bad'
