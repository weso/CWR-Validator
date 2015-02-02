__author__ = 'Borja'
from api import api_app

if __name__ == '__main__':
    api_app.debug = True
    api_app.run(
        host="127.0.0.1",
        port=int("5000")
    )
