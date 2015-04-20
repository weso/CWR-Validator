# -*- coding: utf-8 -*-

import datetime

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

        return encoded

    @staticmethod
    def __encode_entity(entity, encoded):
        encoded['_id'] = entity.creation_id

        return encoded