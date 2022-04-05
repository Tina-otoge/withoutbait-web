import click
import logging
from pathlib import Path
import yaml

from app.db.models import Platform, Tag, Genre
from app import app, db
from . import bp


@bp.cli.command('seed')
@click.argument('files', nargs=-1)
def seed(files):
    handlers = {
        'tags': seed_tags,
        'platforms': seed_platforms,
        'genres': seed_genres,
    }
    if not files:
        seed_dir = Path('./seed/')
        files = seed_dir.rglob('*.yml')
    else:
        files = (Path(x) for x in files)
    for file in files:
        handler = handlers.get(file.stem)
        if not handler:
            logging.warning(f'Ignoring file {file}, does not know how to handle')
            continue
        with file.open() as f:
            data = yaml.safe_load(f)
        if app.debug:
            print(data)
            import json
            with open('debug.json', 'w') as f:
                json.dump(data, f, indent=2)
        handler(data)


def seed_tags(data: dict):
    """
    Expected format
    - <name>:
        ["description"]: <description>
        ["type"]: [type]
    """
    for name, meta in data.items():
        type = meta.get('type')
        if type:
            type = type.upper()
        values = {
            'slug': Tag.slugify(name),
            'name': name,
            'description': meta.get('description'),
            'type': type,
        }
        db.upcreate(Tag, values, match='slug')
        db.session.commit()


def seed_platforms(data: dict):
    """
    Expected format:
    - <short name>: [long name]
    """
    for short_name, long_name in data.items():
        slug = Platform.slugify(short_name)
        if not long_name:
            long_name = short_name
            short_name = None
        values = {
            'slug': slug,
            '_short': short_name,
            'name': long_name,
        }
        db.upcreate(Platform, values, match='slug')
        db.session.commit()


def seed_genres(data: dict):
    for short_name, long_name in data.items():
        slug = Genre.slugify(short_name)
        if not long_name:
            long_name = short_name
            short_name = None
        values = {
            'slug': slug,
            '_short': short_name,
            'name': long_name,
        }
        db.upcreate(Genre, values, match='slug')
        db.session.commit()
