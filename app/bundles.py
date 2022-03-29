from flask_assets import Bundle

from app import APP_DIR, assets

ASSETS_DIR = APP_DIR / 'assets'


def register(name, iterable=None):
    iterable = iterable or (ASSETS_DIR / name).rglob(f'*.{name}')
    bundle = Bundle(*(str(x) for x in iterable), output=f'bundle.{name}')
    assets.register(name, bundle)


def main():
    """Register every assets bundles"""
    register('css')
