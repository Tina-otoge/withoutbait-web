import flask

from app import db
from app.db.models import Game
from . import bp


LIMIT = 10


def get_games_query(**kwargs):
    search = flask.request.args.get('q')
    query = db.session.query(Game)
    if search:
        query = query.filter(Game.name.ilike(f'%{search}%'))
    for method, argument in kwargs.items():
        query = getattr(query, method)(argument)
    return query.limit(LIMIT)


@bp.route('/')
def list_games():
    games = get_games_query()
    return flask.render_template('index.html', entries=games, title='Games')

@bp.route('/popular')
def list_games_by_popularity():
    games = get_games_query(order_by=Game.views.desc())
    return flask.render_template('index.html', entries=games, title='Popular')

@bp.route('/recent')
def list_games_by_date():
    games = get_games_query(order_by=Game.updated_at.desc())
    return flask.render_template('index.html', entries=games, title='Recent')
