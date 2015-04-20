# -*- encoding: utf-8 -*-

import unittest

from cwr.table_value import TableValue

from tests.mongo.utils.mongo_test_conf import host, port, db_name, MongoGenericRepository


__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__status__ = 'Development'


class TestTableValue(unittest.TestCase):
    """
    Tests the ValueEntity API against a Mongo database.
    """

    def setUp(self):
        self._entity = TableValue(1, 'name', 'desc')
        self._repo = MongoGenericRepository(host, port, db_name, 'value_entities')

    def tearDown(self):
        self._repo.clear()

    def test_add(self):
        self.assertEqual(len(self._repo.get(lambda e: True)), 0)
        self._repo.add(self._entity)
        self.assertEqual(len(self._repo.get(lambda e: True)), 1)