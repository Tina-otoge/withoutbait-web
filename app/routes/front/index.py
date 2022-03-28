import flask

from . import bp


@bp.route('/')
def index():
    return flask.render_template('index.html')
