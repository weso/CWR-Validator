# -*- encoding: utf-8 -*-

import unittest

from cwr.work import AlternateTitleRecord

from tests.utils.mongo_test_conf import host, port, db_name, MongoGenericRepository


__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__status__ = 'Development'


class TestAlternativeWorkTitle(unittest.TestCase):
    """
    Tests the AlternativeWorkTitle API against a Mongo database.
    """

    def setUp(self):
        self.entity = AlternateTitleRecord(record_type='SWR',
                                           transaction_sequence_n=3,
                                           record_sequence_n=15,
                                           alternate_title='ALTERNATE',
                                           title_type='FT',
                                           language_code='ES')
        self.repo = MongoGenericRepository(host, port, db_name, 'alternate_titles')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)