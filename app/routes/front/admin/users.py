import flask
from app import db
from app.db.models import User
from . import bp


@bp.route('/users')
def users_list():
    users = (
        db.session.query(User)
        .order_by(User.created_at.desc())
        .limit(100)
    )
    return flask.render_template('admin/users.html', users=users)

