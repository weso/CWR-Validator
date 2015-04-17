from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy


__author__ = 'Borja'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commonworks.db'
app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
# cache = Cache(webapp, config={'CACHE_TYPE': 'memcached', 'CACHE_MEMCACHED_SERVERS': ['localhost:11211']})
app.config['DEBUG'] = True
db = SQLAlchemy(app)

from cwr.validator.api import endpoints