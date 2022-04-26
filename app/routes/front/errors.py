import traceback
import flask

from app import app
from . import bp


@bp.errorhandler(Exception)
def handle_errors(e):
    if app.debug:
        e = '\n'.join(traceback.format_exception(e))
    return flask.render_template('error.html', error=e)
