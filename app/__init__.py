from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from factories import Jinja2
from config import config
from flask.ext.cache import Cache
from app._flask import make_response, extends_db

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
jinja2 = Jinja2()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
cache = Cache()

def create_app(config_name):
    Flask.make_response = make_response
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    extends_db(db)
    jinja2.init_app(app)
    login_manager.init_app(app)
    
    register_routes(app)
    cache.init_app(app)
    
    return app

def register_routes(app):
    from .main import main as main_blueprint
    from .api import api_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    return app