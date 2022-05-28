from datetime import datetime
import json
import sys
import click
import requests

from app import secrets
from app import db
from app.db.models import Game, Platform, GamePlatform
from . import bp


def dump(data):
    json.dump(data, sys.stdout, indent=2)


class Wrapper:
    API_URL = 'https://api.igdb.com/v4/'

    def __init__(self):
        self.client_id = None
        self._client_secret = None
        self._auth_token = None

    @property
    def auth_token(self):
        if self._auth_token:
            return self._auth_token
        tokens = secrets.get_tokens()
        self.client_id = tokens['twitch']['client']
        self._client_secret = tokens['twitch']['secret']
        response = requests.post(
            'https://id.twitch.tv/oauth2/token',
            {
                'client_id': self.client_id,
                'client_secret': self._client_secret,
                'grant_type': 'client_credentials',
            }
        )
        self._auth_token = response.json()['access_token']
        return self.auth_token

    def req(self, endpoint: str, *commands: str, post_process=lambda x: x.json()):
        result = requests.post(
            f'{self.API_URL}{endpoint}', ';'.join(commands) + ';',
            headers={
                'Authorization': f'Bearer {self.auth_token}',
                'Client-ID': self.client_id
            },
        )
        if not result.ok:
            raise Exception(result.content.decode())
        return post_process(result)


wrapper = Wrapper()

@bp.cli.group('igdb')
def group():
    pass


@group.command('platforms')
@click.argument('search', default=None, required=False)
def platforms(search):
    data = wrapper.req(
        'platforms',
        'fields id, name, abbreviation, alternative_name, slug',
        'limit 500',
        f'search "{search}"' if search else ''
    )
    dump(data)


@group.command('search')
@click.argument('term')
def search(term):
    search_and_add_games(term, safe=True)


def search_and_add_games(query, safe=False):
    if not safe:
        query = query.replace(';{}"\'', '')
    data = wrapper.req(
        'games',
        'fields'
        '   name, total_rating, slug, first_release_date, platforms, summary,'
        '   cover.url',
        f'search "{query}"',
    )
    save_games(data)


@group.command('popular')
@click.option('-m', '--minimum-ratings', default=500)
@click.option('-y', '--minimum-year', type=int)
@click.argument('amount', default=100)
def popular(amount, minimum_ratings, minimum_year):
    release_timestamp = int(datetime(minimum_year, 1, 1).timestamp()) if minimum_year else 0
    data = wrapper.req(
        'games',
        'fields'
        '   name, total_rating, slug, first_release_date, platforms, summary,'
        '   cover.url',
        'sort total_rating desc',
        'where'
        '   total_rating != null'
        f'  & total_rating_count > {minimum_ratings}'
        f'  & first_release_date > {release_timestamp}',
        f'limit {amount}',
    )
    save_games(data)


def save_games(data):
    platforms_by_igdb_id = {x.igdb_id: x for x in db.session.query(Platform)}
    result = []
    for game in data:
        date = game.get('first_release_date')
        if date:
            date = datetime.fromtimestamp(date)
        cover = game.get('cover')
        if cover:
            cover = cover['url'].replace('t_thumb', 't_cover_big')
        else:
            cover = 'https://images.igdb.com/igdb/image/upload/t_cover_big/nocover.png'
        values = {
            'name': game['name'],
            'slug': game['slug'],
            'is_slug_from_igdb': True,
            'igdb_score': game.get('total_rating'),
            'summary': game.get('summary'),
            'cover_url': cover,
            'release_date': date,
        }
        obj = db.upcreate(Game, values, match=('is_slug_from_igdb', 'slug'))
        db.session.flush()
        result.append(obj)
        for igdb_platform_id in game.get('platforms', []):
            if igdb_platform_id not in platforms_by_igdb_id:
                continue
            platform = platforms_by_igdb_id[igdb_platform_id]
            if platform in obj.platforms:
                continue
            obj.platforms.append(platform)
        print(obj, obj.igdb_score)
        db.session.commit()
    return result
