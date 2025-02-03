from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from cfg import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.register'

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main_route
    app.register_blueprint(main_route)
    return app