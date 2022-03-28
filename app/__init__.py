from pathlib import Path
import importlib
from flask import Flask
from flask_assets import Environment


APP_DIR = Path(__file__).parent

app = Flask(__name__)
assets = Environment(app)


def register_blueprints():
    for name in ('api', 'front'):
        module = importlib.import_module(f'.routes.{name}', __name__)
        if hasattr(module, 'bp'):
            app.register_blueprint(module.bp)


from .blueprint import Blueprint
from . import bundles

register_blueprints()
