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

    from logging.handlers import RotatingFileHandler
    from logging import Formatter

    from flask import Flask
    from flask.ext import restful

    from werkzeug.contrib.fixers import ProxyFix

    from cwr_validator.uploads import __uploads__

    from cwr_validator.endpoint import UploadFileResource

    from cwr_validator.service.file import LocalFileService

    from data_validator.accessor import CWRValidatorConfiguration

    config = CWRValidatorConfiguration()
    config = config.get_config()

    debug = bool(config['debug'])
    secret = config['secretKey']
    if len(secret) == 0:
        secret = os.urandom(24)
    upload = config['upload.folder']
    if len(upload) == 0:
        upload = __uploads__.path()
    log = config['log.folder']
    if len(log) == 0:
        log = 'cwr_webapp.log'

    app = Flask(__name__)
    api = restful.Api(app)

    api.add_resource(UploadFileResource, '/upload')

    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config['DEBUG'] = debug
    app.config['SECRET_KEY'] = secret
    app.config['UPLOAD_FOLDER'] = upload

    app.config['FILE_SERVICE'] = LocalFileService(app.config['UPLOAD_FOLDER'])

    if debug:
        handler = RotatingFileHandler(log, maxBytes=10000, backupCount=1)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(Formatter('[%(levelname)s][%(asctime)s] %(message)s'))

        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('').addHandler(handler)

        app.logger.addHandler(handler)

    logging.info('Debug mode is set to %r' % debug)

    return app

