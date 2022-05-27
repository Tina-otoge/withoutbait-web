from flask_login import UserMixin
import sqlalchemy as sa
import werkzeug.security

from app import db


class User(db.Base, db.IdMixin, db.CreatedMixin, UserMixin):
    REPR_KEYS = {'username'}

    username = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String)
    is_admin = sa.Column(sa.Boolean)

    def __init__(self, **kwargs):
        kwargs['password'] = werkzeug.security.generate_password_hash(kwargs['password'])
        super().__init__(**kwargs)

    def __str__(self):
        return self.username

    def check_password(self, s: str):
        return werkzeug.security.check_password_hash(self.password, s)

    @property
    def avatar_url(self):
        # TODO
        return 'https://osu.ppy.sh/images/layout/avatar-guest.png'
