import enum
import sqlalchemy as sa

from app import db


class Tag(db.Base, db.IdMixin, db.SlugMixin, db.TimedMixin):
    class Type(enum.Enum):
        """For special types of tags, do not use any type for "regular" tags"""
        WARN = enum.auto()

    name = sa.Column(sa.String)
    description = sa.Column(sa.String)
    score = sa.Column(sa.Integer, **db.default_value(0))
    type = sa.Column(sa.Enum(Type))
    force_icon = sa.Column(sa.String)
    force_rating = sa.Column(sa.String)

    def __str__(self):
        return self.name

    @property
    def icon(self):
        # https://fonts.google.com/icons?selected=Material+Icons
        if self.force_icon:
            return self.force_icon
        if self.type == self.Type.WARN:
            return 'warning'
        if self.score < 0:
            return 'thumb_down'
        if self.score > 0:
            return 'thumb_up'
        return 'sentiment_neutral'

    @property
    def rating(self):
        if self.force_rating:
            return self.force_rating
        if self.score < 0:
            return 'danger'
        if self.score > 0:
            return 'clean'
        return 'meh'

