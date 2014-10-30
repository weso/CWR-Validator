__author__ = 'Borja'
from api import api_app

if __name__ == '__main__':
    api_app.debug = True
    api_app.run(
        host="0.0.0.0",
        port=int("5000")
    )
