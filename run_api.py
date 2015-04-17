# -*- encoding: utf-8 -*-
import os
import logging

from cwr_validator.validator.service import app
from flask.ext.sqlalchemy import SQLAlchemy


"""
Runs the CWR Validator web API.
"""

__author__ = 'Bernardo Martínez Garrido, Borja Garrido Bear'
__license__ = 'MIT'
__version__ = '0.0.0'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = bool(os.environ.get('DEBUG', True))
    secret = os.environ.get('SECRET_KEY', 'development_key')

    upload = os.environ.get('UPLOAD_FOLDER', './files')

    app.config['DEBUG'] = debug
    app.config['SECRET_KEY'] = secret

    app.config['UPLOAD_FOLDER'] = upload

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commonworks.db'
    app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
    # cache = Cache(webapp, config={'CACHE_TYPE': 'memcached', 'CACHE_MEMCACHED_SERVERS': ['localhost:11211']})
    db = SQLAlchemy(app)

    if debug:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(filename='cwr_validator.log', level=logging.INFO, maxBytes=10000, backupCount=1)

    logging.info('Debug mode is set to %r' % debug)

    app.run(host=host, port=port)
