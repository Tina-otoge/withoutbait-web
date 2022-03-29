import sqlalchemy as sa

from app import db


class ReviewTag(db.Base, db.CreatedMixin):
    review_id = sa.Column(sa.ForeignKey('reviews.id'), primary_key=True)
    tag_id = sa.Column(sa.ForeignKey('tags.id'), primary_key=True)

