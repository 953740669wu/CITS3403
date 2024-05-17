import sys
import os
from flask import Flask, session, g
from app.config import Config
from app.extensions import db, migrate, login_manager
from app.models import UserModel
from flask_login import LoginManager
from app.blueprints import main

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)


db.init_app(app)
migrate.init_app(app, db)
app.register_blueprint(main)
login_manager.init_app(app)  
login_manager.login_view = 'main.login' 

from app import routes



if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(debug=True)
