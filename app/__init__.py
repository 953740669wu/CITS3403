import sys
import os
from flask import Flask, session, g
from app.config import Config
from app.extensions import db, migrate, login_manager
from app.models import UserModel
from flask_login import LoginManager
from app.blueprints import main

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.blueprints import main
    app.register_blueprint(main)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    with app.app_context():
        from app import routes  

    return app
