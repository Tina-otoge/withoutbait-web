import flask
import flask_login

from app import app, db
from app.cli.igdb_seed import search_and_add_games
from app.db.models import Game, Platform, Review, User
from . import bp, get_front_loads_count


class GamesQuery:
    LIMIT = 25

    def __init__(self):
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
        self.search = search
        self.query = query
        self.page = page

    def run(self):
        return self.query.offset(self.LIMIT * (self.page - 1)).limit(self.LIMIT)



def get_games_query(**kwargs):
    query = GamesQuery()
    for method, argument in kwargs.items():
        query.query = getattr(query.query, method)(argument)
    return query.run()


def get_stats():
    return {
        'total_games_reviewed': db.session.query(Game).filter(Game.score != None).count(),
        'total_reviews': db.session.query(Review).count(),
        'front_loads_count': get_front_loads_count().value,
        'total_users': db.session.query(User).count()
    }


@bp.route('/')
@bp.route('/popular')
def list_games_by_popularity():
    query = GamesQuery()
    query.query = query.query.order_by(Game.igdb_score.desc())
    query.query = query.query.filter(Game.score != None)
    games = query.run()
    return flask.render_template(
        'index.html', entries=games, title='Popular',
        stats=get_stats(),
    )

@bp.route('/recent')
def list_games_by_date():
    query = GamesQuery()
    query.query = query.query.filter(Game.score != None)
    query.query = query.query.order_by(Game.updated_at.desc(), Game.created_at.desc())
    games = query.run()
    return flask.render_template(
        'index.html', entries=games, title='Recent',
        stats=get_stats(),
    )


@bp.route('/contribute')
@flask_login.login_required
def list_unrated_games():
    query = GamesQuery()
    if query.search:
        try:
            search_and_add_games(query.search)
        except Exception as e:
            if app.config['DEBUG']:
                raise e
    query.query = query.query.filter(Game.score == None)
    query.query = query.query.order_by(Game.igdb_score.desc())
    games = query.run()
    return flask.render_template(
        'index.html', entries=games, title='Unrated games',
        stats=get_stats(),
    )
