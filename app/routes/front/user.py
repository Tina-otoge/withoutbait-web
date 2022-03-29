import flask
import flask_login

from . import bp


@bp.route('/account')
@flask_login.login_required
def account():
    return flask.render_template('account.html')
