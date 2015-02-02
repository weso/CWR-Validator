from webapp import app

__author__ = 'Borja'

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "development_key"
    app.run(
        host="127.0.0.1",
        port=int("5001")
    )
