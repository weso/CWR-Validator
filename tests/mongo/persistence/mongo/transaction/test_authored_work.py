# -*- encoding: utf-8 -*-

import unittest

from cwr.work import AuthoredWorkRecord
from cwr.other import ISWCCode

from tests.mongo.utils.mongo_test_conf import host, port, db_name
from cwr_validator.persistence.repository import MongoGenericRepository


__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__status__ = 'Development'


class TestAuthoredWork(unittest.TestCase):
    """
    Tests the EntireWorkTitle API against a Mongo database.
    """

    def setUp(self):
        iswc = ISWCCode(12345678, 9)

        self.entity = AuthoredWorkRecord(record_type='SWR',
                                         transaction_sequence_n=3,
                                         record_sequence_n=15,
                                         title='TITLE',
                                         submitter_work_n='ABC135',
                                         writer_1_first_name='FIRST NAME 1',
                                         writer_1_last_name='LAST NAME 1',
                                         writer_2_first_name='FIRST NAME 2',
                                         writer_2_last_name='LAST NAME 2',
                                         writer_1_ipi_base_n='I-000000229-7',
                                         writer_1_ipi_name_n=14107338,
                                         writer_2_ipi_base_n='I-000000300-7',
                                         writer_2_ipi_name_n=14107448,
                                         source='SOURCE',
                                         language_code='ES',
                                         iswc=iswc)
        self.repo = MongoGenericRepository(host, port, db_name, 'authored_works')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)