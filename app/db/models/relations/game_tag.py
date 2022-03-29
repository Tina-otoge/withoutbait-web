import sqlalchemy as sa

from app import db


class GameTag(db.Base, db.CreatedMixin):
    game_id = sa.Column(sa.ForeignKey('games.id'), primary_key=True)
    tag_id = sa.Column(sa.ForeignKey('tags.id'), primary_key=True)
