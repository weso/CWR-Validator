# -*- encoding: utf-8 -*-

import unittest
import datetime

from cwr.agreement import AgreementRecord

from tests.mongo.utils.mongo_test_conf import host, port, db_name
from cwr_validator.persistence.repository import MongoGenericRepository


__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__status__ = 'Development'


class TestAgreement(unittest.TestCase):
    """
    Tests the Agreement API against a Mongo database.
    """

    def setUp(self):
        self._entity = AgreementRecord(record_type='ACK',
                                       transaction_sequence_n=3,
                                       record_sequence_n=15,
                                       submitter_agreement_n='AB12',
                                       agreement_type='OS',
                                       agreement_start_date=datetime.datetime.strptime('20030215', '%Y%m%d').date(),
                                       number_of_works=12,
                                       prior_royalty_status='D',
                                       post_term_collection_status='D',
                                       international_standard_code='DFG135',
                                       society_assigned_agreement_n='DF35',
                                       sales_manufacture_clause='M',
                                       agreement_end_date=datetime.datetime.strptime('20030216', '%Y%m%d').date(),
                                       date_of_signature=datetime.datetime.strptime('20030217', '%Y%m%d').date(),
                                       retention_end_date=datetime.datetime.strptime('20030218', '%Y%m%d').date(),
                                       prior_royalty_start_date=datetime.datetime.strptime('20030219', '%Y%m%d').date(),
                                       post_term_collection_end_date=datetime.datetime.strptime('20030220',
                                                                                                '%Y%m%d').date(),
                                       shares_change=True,
                                       advance_given=True)
        self._repo = MongoGenericRepository(host, port, db_name, 'agreements')

    def tearDown(self):
        self._repo.clear()

    def test_add(self):
        self.assertEqual(len(self._repo.get(lambda e: True)), 0)
        self._repo.add(self._entity)
        self.assertEqual(len(self._repo.get(lambda e: True)), 1)