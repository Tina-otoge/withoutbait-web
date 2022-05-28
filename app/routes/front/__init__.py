from app import Blueprint


bp = Blueprint(__name__)


def get_front_loads_count():
    from app import db
    from app.db.models import Key

    count = db.upcreate(
        Key, {'name': 'front_loads_count', 'coerce': Key.Types.INT},
        match=True,
        default={'value': 0},
    )
    return count


@bp.before_request
def increase_front_loads_count():
    from app import db
    count = get_front_loads_count()
    count.value = count.value + 1
    db.commit()

from . import errors, faq, game, list_games, login, user
