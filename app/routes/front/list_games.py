import flask

from app import db
from app.db.models import Game, Platform
from . import bp


LIMIT = 25


def get_games_query(**kwargs):
    search = flask.request.args.get('q')
    page = flask.request.args.get('p', 1)
    platform = flask.request.args.get('platform')
    try:
        page = int(page)
    except ValueError:
        page = 1
    query = db.session.query(Game)
    if platform:
        query = query.join(Game.platforms)
        query = query.filter(Platform.slug == platform)
    if search:
        query = query.filter(Game.name.ilike(f'%{search}%'))
    for method, argument in kwargs.items():
        query = getattr(query, method)(argument)
    return query.offset(LIMIT * (page - 1)).limit(LIMIT)


# def list_games():
#     games = get_games_query()
#     return flask.render_template('index.html', entries=games, title='Games')


@bp.route('/')
@bp.route('/popular')
def list_games_by_popularity():
    games = get_games_query(order_by=Game.igdb_score.desc())
    return flask.render_template('index.html', entries=games, title='Popular')

@bp.route('/recent')
def list_games_by_date():
    games = get_games_query(order_by=Game.updated_at.desc())
    return flask.render_template('index.html', entries=games, title='Recent')
