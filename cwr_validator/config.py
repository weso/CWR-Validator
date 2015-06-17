# -*- encoding: utf-8 -*-
import os

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class Config(object):
    os_env = os.environ

    SECRET_KEY = os_env.get('CWR_VALIDATOR_SECRET', os.urandom(24))
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class DevConfig(Config):
    """
    Development configuration.
    """
    ENV = 'dev'
    DEBUG = True


class ProdConfig(Config):
    """
    Development configuration.
    """
    ENV = 'prod'
    DEBUG = False


class TestConfig(Config):
    TESTING = True
    DEBUG = True
