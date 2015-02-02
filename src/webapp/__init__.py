from flask import Flask

__author__ = 'Borja'

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'development_key'

from webapp import views