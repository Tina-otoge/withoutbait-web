import sqlalchemy as sa

from app import db


class User(db.Base, db.IdMixin, db.CreatedMixin):
    username = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String)
