import sqlalchemy as sa

from app import db


class GamePlatform(db.Base, db.CreatedMixin):
    game_id = sa.Column(sa.ForeignKey('games.id'), primary_key=True)
    platform_id = sa.Column(sa.ForeignKey('platforms.id'), primary_key=True)

