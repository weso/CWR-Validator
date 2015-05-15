# -*- coding: utf-8 -*-

import datetime

from cwr.other import *

from cwr.parser.dictionary import CWRDictionaryEncoder


"""
Offers classes to create Mongo dictionaries from model objects.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class MongoDictionaryEncoder(CWRDictionaryEncoder):
    """
    Encodes CWR model classes into Mongo dictionaries.
    """

    def __init__(self):
        super(MongoDictionaryEncoder, self).__init__()

    def encode(self, d):
        encoded = super(MongoDictionaryEncoder, self).encode(d)

        for key, value in encoded.iteritems():
            if isinstance(value, datetime.date):
                encoded[key] = value.isoformat()
            elif isinstance(value, datetime.time):
                encoded[key] = value.isoformat()
            elif isinstance(value, datetime.datetime):
                encoded[key] = value.isoformat()
            elif isinstance(value, ISWCCode):
                # TODO: This should be transformed into a dict by the parser
                encoded[key] = str(value)
            elif isinstance(value, VISAN):
                # TODO: This should be transformed into a dict by the parser
                encoded[key] = str(value)

        return encoded

    @staticmethod
    def __encode_entity(entity, encoded):
        encoded['_id'] = entity.creation_id

        return encoded