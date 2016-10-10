from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from factories import Jinja2
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
jinja2 = Jinja2()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    jinja2.init_app(app)
    
    register_routes(app)
    
    return app

def register_routes(app):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app