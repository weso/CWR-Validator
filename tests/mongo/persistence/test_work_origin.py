# -*- encoding: utf-8 -*-

import unittest

from cwr.work import WorkOriginRecord
from cwr.other import VISAN

from tests.mongo.utils.mongo_test_conf import host, port, db_name, MongoGenericRepository


__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__status__ = 'Development'


class TestWorkOrigin(unittest.TestCase):
    """
    Tests the WorkOrigin API against a Mongo database.
    """

    def setUp(self):
        visan = VISAN(1234567, 12345678912, 123, 1)

        self.entity = WorkOriginRecord(record_type='ORN',
                                       transaction_sequence_n=3,
                                       record_sequence_n=15,
                                       intended_purpose='PURPOSE',
                                       production_title='TITLE',
                                       cd_identifier='ID134',
                                       cut_number=5,
                                       library='LIB467',
                                       bltvr='BLTVR',
                                       visan=visan,
                                       production_n='PROD145',
                                       episode_title='EPISODE',
                                       episode_n='EP145',
                                       year_production=1994,
                                       audio_visual_key='KEY')
        self.repo = MongoGenericRepository(host, port, db_name, 'work_origins')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)