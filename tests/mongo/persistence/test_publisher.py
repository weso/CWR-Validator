# -*- encoding: utf-8 -*-

import unittest

from cwr.interested_party import Publisher

from tests.mongo.utils.mongo_test_conf import host, port, db_name, MongoGenericRepository


__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__status__ = 'Development'


class TestPublisher(unittest.TestCase):
    """
    Tests the Publisher API against a Mongo database.
    """

    def setUp(self):
        self.entity = Publisher(ip_n='ABC15',
                                publisher_name='NAME',
                                ipi_name_n=14107338,
                                ipi_base_n='I-000000229-7',
                                tax_id=923703412)
        self.repo = MongoGenericRepository(host, port, db_name, 'publishers')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)