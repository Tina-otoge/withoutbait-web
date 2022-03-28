from app import Blueprint


bp = Blueprint(__name__)

from . import game, index
