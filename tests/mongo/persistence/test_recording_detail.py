# -*- encoding: utf-8 -*-

import unittest
import datetime

from cwr.work import RecordingDetailRecord

from tests.utils.mongo_test_conf import host, port, db_name, MongoGenericRepository


__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__status__ = 'Development'


class TestRecordingDetails(unittest.TestCase):
    """
    Tests the RecordingDetails API against a Mongo database.
    """

    def setUp(self):
        self.entity = RecordingDetailRecord(record_type='SWR',
                                            transaction_sequence_n=3,
                                            record_sequence_n=15,
                                            first_release_date=datetime.datetime.strptime('20030216', '%Y%m%d').date(),
                                            first_release_duration=datetime.datetime.strptime('011200',
                                                                                              '%H%M%S').time(),
                                            first_album_title='FIRST TITLE',
                                            first_album_label='FIRST LABEL',
                                            first_release_catalog_n='ABF35',
                                            ean=1234567890123,
                                            isrc='ES-A2B-12-12',
                                            recording_format='V',
                                            recording_technique='D',
                                            media_type='CES')
        self.repo = MongoGenericRepository(host, port, db_name, 'recording_details')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)