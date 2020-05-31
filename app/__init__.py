# -*- coding: utf-8 -*-
import os
from logging import INFO, Formatter, handlers

from flask import Flask
from werkzeug.exceptions import default_exceptions

from app.api import bp as api_bp
from app.errors.handler import api_error_handler


def create_app(environment=None):
    """ Create a new Flask application. """

    app = Flask(__name__)

    environment = environment if environment is not None else app.config['ENV']
    if environment == 'production':
        app.config.from_object('app.config.ProductionConfig')
    elif environment == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.DevelopmentConfig')

    __config_logging(app)
    __init_extensions(app)
    __register_blueprint(app)
    __handle_errors(app)

    return app


def __config_logging(app):
    """ Config logging for Flask application. """

    if app.config['ENV'] == 'production':
        fmt = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        formatter = Formatter(fmt=fmt)

        info_log = os.path.join(app.config['LOG_FOLDER'], 'app-info.log')
        info_log_handler = handlers.RotatingFileHandler(
            filename=info_log,
            maxBytes=1024 ** 2,
            backupCount=10)
        info_log_handler.setLevel(level=INFO)
        info_log_handler.setFormatter(fmt=formatter)
        app.logger.addHandler(info_log_handler)

    app.logger.setLevel(INFO)
    app.logger.info('Starting Pub V3 API...')


def __init_extensions(app):
    """ Initiate the config of Flask extensions. """

    from app.extensions import db, ma, migrate, api, jwt_manager, cors
    db.init_app(app)
    ma.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    api.init_app(api_bp)
    jwt_manager.init_app(app)


def __register_blueprint(app):
    """ Register the routes of Flask application. """

    app.register_blueprint(api_bp)


def __handle_errors(app):
    for exp in default_exceptions:
        app.register_error_handler(exp, api_error_handler)
    app.register_error_handler(Exception, api_error_handler)
