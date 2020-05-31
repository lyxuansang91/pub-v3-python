# -*- coding: utf-8 -*-
import os
import datetime

root_app = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def _make_dir(dir_name):
    """ Make folder used to store log files. """

    log_dir_path = os.path.join(root_app, dir_name)
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)
    return log_dir_path


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    LOG_FOLDER = _make_dir('logs')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(root_app, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=2)


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
