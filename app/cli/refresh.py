from app import db
from app.db.models import Game

from . import bp


@bp.cli.command('refresh')
def refresh():
    for game in db.session.query(Game):
        game.update_rating()
    db.commit()
