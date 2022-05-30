import flask
import flask_login

from app import Blueprint


bp = Blueprint(__name__, prefix='/admin')


@bp.before_request
def admin_check():
    if not flask_login.current_user.is_admin:
        flask.flash('You do not have permission to access this page')
        return flask.redirect('/')

from . import index, reviews_log, useradd, users
