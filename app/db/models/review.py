import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Review(db.Base, db.IdMixin, db.TimedMixin):
    author_id = sa.Column(sa.ForeignKey('users.id'))
    game_id = sa.Column(sa.ForeignKey('games.id'), nullable=False)
    comment = sa.Column(sa.Text)

    tags = orm.relationship('Tag', secondary='review_tags')
    author = orm.relationship('User', backref='reviews')
    game = orm.relationship('Game', back_populates='reviews', order_by="Review.id.desc()")
