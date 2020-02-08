
import logging
from logging import StreamHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from plugin._flask import make_response, extends_db, CustomJSONEncoder

from config import config

db = SQLAlchemy()

def create_app(config_name):
    Flask.make_response = make_response
    app = Flask(__name__, static_folder='resource')
    app.json_encoder = CustomJSONEncoder
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    extends_db(db)
    
    register_routes(app)
    init_logger(app)
    return app

def register_routes(app):
    from .blueprints.main import main as main_blueprint
    from .blueprints.admin import admin_blueprint
    from .blueprints.client import client_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/api/admin')
    app.register_blueprint(client_blueprint, url_prefix='/api/client')
    return app

def init_logger(app):
    from flask.logging import default_handler
    handler = StreamHandler()
    handler.setLevel(app.config['LOG_LEVEL'])
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(handler)
