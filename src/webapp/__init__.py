from flask import Flask

__author__ = 'Borja'

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'development_key'

from webapp import views