# -*- encoding: utf-8 -*-
import os
import logging

from cwr.validator.service import app


"""
Runs the CWR Validator web API.
"""

__author__ = 'Borja Garrido Bear'
__license__ = 'MIT'
__version__ = '0.0.0'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = bool(os.environ.get('DEBUG', True))
    secret = os.environ.get('SECRET_KEY', 'development_key')

    app.config['DEBUG'] = debug
    app.config['SECRET_KEY'] = secret

    if debug:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(filename='cwr.log', level=logging.INFO, maxBytes=10000, backupCount=1)

    logging.info('Debug mode is set to %r' % debug)

    app.run(host=host, port=port)
