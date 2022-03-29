import sqlalchemy as sa

from app import db


class Platform(db.Base, db.IdMixin, db.SlugMixin):
    _short = sa.Column('short', sa.String)
    name = sa.Column(sa.String, nullable=False)

    @property
    def short(self):
        return self._short or self.name
