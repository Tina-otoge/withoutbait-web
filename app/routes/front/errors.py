import flask

from . import bp


@bp.errorhandler(Exception)
def handle_errors(e):
    return flask.render_template('error.html', error=e)
