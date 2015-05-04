# -*- coding: utf-8 -*-
"""
    CWR Data API Validator WS
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    Validator Web Service for Common Works Registrations.
    :copyright: (c) 2015 by WESO
    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.0.1'
__license__ = 'MIT'


def create_app():
    import os
    import logging

    from flask import Flask
    from werkzeug.contrib.fixers import ProxyFix
    from flask.ext.sqlalchemy import SQLAlchemy

    from cwr_validator.endpoint import upload_blueprint

    from cwr_validator.service.file import LocalFileService

    debug = bool(os.environ.get('CWR_VALIDATOR_DEBUG', True))
    secret = os.environ.get('CWR_VALIDATOR_SECRET_KEY', os.urandom(24))
    upload = os.environ.get('UPLOAD_FOLDER', './files')

    app = Flask(__name__)
    app.register_blueprint(upload_blueprint, url_prefix='/upload')

    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config['DEBUG'] = debug
    app.config['SECRET_KEY'] = secret
    app.config['UPLOAD_FOLDER'] = upload

    app.config['FILE_SERVICE'] = LocalFileService(app.config['UPLOAD_FOLDER'])

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commonworks.db'
    app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
    # cache = Cache(webapp, config={'CACHE_TYPE': 'memcached', 'CACHE_MEMCACHED_SERVERS': ['localhost:11211']})
    db = SQLAlchemy(app)

    if debug:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(filename='cwr_validator.log', level=logging.INFO, maxBytes=10000, backupCount=1)

    logging.info('Debug mode is set to %r' % debug)

    return app

