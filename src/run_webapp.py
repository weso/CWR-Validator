# -*- encoding: utf-8 -*-
from webapp import app

"""
Runs the CWR Validator web UI.
"""

__author__ = 'Borja Garrido Bear'
__license__ = 'MIT'
__version__ = '0.0.0'

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("5001")
    )
