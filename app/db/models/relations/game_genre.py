import sqlalchemy as sa

from app import db


class GameGenre(db.Base, db.CreatedMixin):
    game_id = sa.Column(sa.ForeignKey('games.id'), primary_key=True)
    genre_id = sa.Column(sa.ForeignKey('genres.id'), primary_key=True)


