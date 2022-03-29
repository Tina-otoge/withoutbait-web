from app import Blueprint


bp = Blueprint(__name__)

from . import errors, game, index, login, user
