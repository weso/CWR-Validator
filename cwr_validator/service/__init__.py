from flask import Flask


__author__ = 'Borja'

app = Flask(__name__)

from cwr_validator.service import endpoints