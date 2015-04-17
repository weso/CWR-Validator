# -*- encoding: utf-8 -*-
from cwr.validator.api import api_app

"""
Runs the CWR Validator web API.
"""

__author__ = 'Borja Garrido Bear'
__license__ = 'MIT'
__version__ = '0.0.0'

if __name__ == '__main__':
    api_app.debug = True
    api_app.run(
        host="127.0.0.1",
        port=int("5000")
    )
