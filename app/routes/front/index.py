import flask

from app import db
from app.db.models import Game
from . import bp


@bp.route('/')
def index():
    games = db.session.query(Game).limit(10)
    return flask.render_template('index.html', entries=games)
