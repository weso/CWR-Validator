# -*- encoding: utf-8 -*-

import unittest

from cwr.agreement import InterestedPartyForAgreementRecord

from tests.mongo.utils.mongo_test_conf import host, port, db_name
from cwr_validator.persistence.repository import MongoGenericRepository


__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__status__ = 'Development'


class TestIPA(unittest.TestCase):
    """
    Tests the IPA API against a Mongo database.
    """

    def setUp(self):
        self.entity = InterestedPartyForAgreementRecord(record_type='ACK',
                                                        transaction_sequence_n=3,
                                                        record_sequence_n=15,
                                                        ip_n='AB12',
                                                        ip_last_name='LAST NAME',
                                                        agreement_role_code='AS',
                                                        ip_writer_first_name='FIRST NAME',
                                                        ipi_name_n='00014107338',
                                                        ipi_base_n='I-000000229-7',
                                                        pr_society=12,
                                                        pr_share=50.5,
                                                        mr_society=13,
                                                        mr_share=60.5,
                                                        sr_society=14,
                                                        sr_share=70.5)
        self.repo = MongoGenericRepository(host, port, db_name, 'ipas')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)