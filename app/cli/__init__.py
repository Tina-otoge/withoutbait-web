from app import Blueprint


bp = Blueprint(__name__)

from . import igdb_seed, refresh, seed
