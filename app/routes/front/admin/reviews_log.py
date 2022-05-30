import flask
from app import db
from app.db.models import Review
from . import bp


@bp.route('/reviews')
def reviews_log():
    reviews = (
        db.session.query(Review)
        .order_by(Review.created_at.desc())
        .limit(100)
    )
    return flask.render_template('admin/reviews.html', reviews=reviews)
