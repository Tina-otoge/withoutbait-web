import flask

from app import db
from app.db.models import Game
from . import bp


LIMIT = 10


@bp.route('/')
def list_games():
    games = db.session.query(Game).limit(LIMIT)
    return flask.render_template('index.html', entries=games, title='Games')

@bp.route('/popular')
def list_games_by_popularity():
    games = db.session.query(Game).order_by(Game.views.desc()).limit(LIMIT)
    return flask.render_template('index.html', entries=games, title='Popular')

@bp.route('/recent')
def list_games_by_date():
    games = db.session.query(Game).order_by(Game.updated_at.desc()).limit(LIMIT)
    return flask.render_template('index.html', entries=games, title='Recent')
