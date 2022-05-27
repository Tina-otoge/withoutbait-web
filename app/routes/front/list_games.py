import flask

from app import db
from app.db.models import Game, Platform, Review
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
        'total_games': db.session.query(Game).count(),
        'total_reviews': db.session.query(Review).count(),
        'total_games_unrated': db.session.query(Game).filter(Game.score == None).count(),
        'front_loads_count': get_front_loads_count().value,
    }


@bp.route('/')
@bp.route('/popular')
def list_games_by_popularity():
    query = GamesQuery()
    query.query = query.query.order_by(Game.igdb_score.desc())
    games = query.run()
    return flask.render_template(
        'index.html', entries=games, title='Popular',
        stats=get_stats(),
    )

@bp.route('/recent')
def list_games_by_date():
    query = GamesQuery()
    query.query = query.query.order_by(Game.updated_at.desc(), Game.created_at.desc())
    games = query.run()
    return flask.render_template(
        'index.html', entries=games, title='Recent',
        stats=get_stats(),
    )
