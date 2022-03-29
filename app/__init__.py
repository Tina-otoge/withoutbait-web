from pathlib import Path
import importlib
from flask import Flask
from flask_assets import Environment

from app import config


APP_DIR = Path(__file__).parent

app = Flask(__name__)
assets = Environment(app)
app.config.from_object(config)


def register_blueprints():
    for name in ('routes.api', 'routes.front', 'cli'):
        module = importlib.import_module(f'.{name}', __name__)
        if hasattr(module, 'bp'):
            app.register_blueprint(module.bp)


from .db import models
from .blueprint import Blueprint
from . import bundles

register_blueprints()
bundles.main()
