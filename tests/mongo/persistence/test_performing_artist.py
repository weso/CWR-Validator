# -*- encoding: utf-8 -*-

import unittest

from cwr.work import PerformingArtistRecord

from tests.mongo.utils.mongo_test_conf import host, port, db_name, MongoGenericRepository


__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__status__ = 'Development'


class TestPerformingArtist(unittest.TestCase):
    """
    Tests the PerformingArtist API against a Mongo database.
    """

    def setUp(self):
        self.entity = PerformingArtistRecord(record_type='PER',
                                             transaction_sequence_n=3,
                                             record_sequence_n=15,
                                             performing_artist_last_name='LAST NAME',
                                             performing_artist_first_name='FIRST NAME',
                                             performing_artist_ipi_name_n=14107338,
                                             performing_artist_ipi_base_n='I-000000339-7')
        self.repo = MongoGenericRepository(host, port, db_name, 'performing_artists')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)