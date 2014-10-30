from flask import Flask

__author__ = 'Borja'

app = Flask(__name__)
app.config['DEBUG'] = True

from webapp import views