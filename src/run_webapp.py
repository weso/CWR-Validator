from webapp import app

__author__ = 'Borja'

if __name__ == '__main__':
    app.debug = True
    app.run(
        host="127.0.0.1",
        port=int("5001")
    )
