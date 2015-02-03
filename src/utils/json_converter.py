# -*- encoding: utf-8 -*-
import datetime
import json

from models.cwr_objects import CWRField


"""
JSON converter to handle coding objects into JSON strings collections.
"""

__author__ = 'Borja Garrido Bear'
__license__ = 'MIT'
__version__ = '0.0.0'
__status__ = 'Development'


class JsonConverter():
    """
    JSON converter to handle datetime objects.
    """

    def __init__(self):
        self._dt_handler = lambda obj: (
            obj.isoformat()

            if isinstance(obj, datetime.time) or isinstance(obj, datetime.date)
            else obj.value

            if isinstance(obj, CWRField)
            else obj.__dict__
        )

    def print_object(self, python_object):
        json_object = json.dumps(python_object, default=self._dt_handler)

        with open('data.txt', 'wb') as file:
            file.write(json_object)

    def parse_object(self, python_object):
        json_object = json.dumps(python_object, default=self._dt_handler)

        return json_object
