# -*- encoding: utf-8 -*-

try:
    import thread

    _python2 = True
except ImportError:
    import threading as thread
    from threading import Thread

    _python2 = False

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


def threaded(function):
    def _decorator(*args):
        if _python2:
            thread.start_new_thread(function, args)
        else:
            Thread(target=function, args=args).start()

    return _decorator
