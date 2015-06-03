# -*- coding: utf-8 -*-
try:
    from StringIO import StringIO

    IOModule = StringIO
    _python2 = True
except ImportError:
    from io import BytesIO

    IOModule = BytesIO
    _python2 = False

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


def prepare_file(text):
    if _python2:
        result = IOModule('my file contents')
    else:
        result = IOModule(b'my file contents')

    return result
