from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy


__author__ = 'Borja'

api_app = Flask(__name__)
api_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commonworks.db'
api_app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
# cache = Cache(webapp, config={'CACHE_TYPE': 'memcached', 'CACHE_MEMCACHED_SERVERS': ['localhost:11211']})
api_app.config['DEBUG'] = True
db = SQLAlchemy(api_app)

from api import endpoints