from pathlib import Path
import importlib
from flask import Flask
from flask_assets import Environment
from flask_login import LoginManager

from app import config, secrets


APP_DIR = Path(__file__).parent

app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY'] = secrets.get_secret_key()
assets = Environment(app)
login_manager = LoginManager(app)
login_manager.login_message = "You need an account to access this page"
login_manager.login_view = '/register'


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
