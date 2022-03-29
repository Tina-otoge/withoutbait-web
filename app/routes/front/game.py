import flask

from . import bp


@bp.route('/games/<slug>')
def game(slug: str):
    flask.render_template('game.html', entry={})
