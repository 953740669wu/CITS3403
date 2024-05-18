import sys
import os
from flask import Flask, session, g
from app.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from app.extensions import db, migrate, login_manager
from flask_login import LoginManager
from flask_mail import Mail

mail = Mail()


def create_app(config_name=None, config_class=None):
    app = Flask(__name__)
    
    if config_class:
        app.config.from_object(config_class)
    elif config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    mail.init_app(app)

    from app.blueprints import main
    app.register_blueprint(main)

    with app.app_context():
        from app import routes  # Ensure routes are imported within app context to avoid circular import

    return app
