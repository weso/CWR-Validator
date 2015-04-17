# -*- encoding: utf-8 -*-
import unittest
import datetime

from cwr.agreement import AgreementRecord, InterestedPartyForAgreementRecord
from cwr.interested_party import Publisher
from cwr.table_value import TableValue
from cwr.work import AlternateTitleRecord, AuthoredWorkRecord, \
    PerformingArtistRecord, WorkOriginRecord, WorkRecord, RecordingDetailRecord
from cwr.other import ISWCCode, VISAN

from tests.utils.mongo_test_conf import host, port, db_name, MongoGenericRepository


"""
Integration tests to check that it is possible to store the model classes in a Mongo database.

Requires a Mongo database running, and set up as mongo_test_conf indicates.

Right now these are just placeholders to create real tests.
"""

__author__ = 'Bernardo Martínez Garrido,Borja Garrido Bear'
__license__ = 'MIT'
__version__ = '0.0.0'
__status__ = 'Development'


class TestAgreement(unittest.TestCase):
    """
    Tests the Agreement API against a Mongo database.
    """

    def setUp(self):
        self.entity = AgreementRecord(record_type='ACK',
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
        self.repo = MongoGenericRepository(host, port, db_name, 'agreements')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)


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


class TestValueEntity(unittest.TestCase):
    """
    Tests the ValueEntity API against a Mongo database.
    """

    def setUp(self):
        self.entity = TableValue(1, 'name', 'desc')
        self.repo = MongoGenericRepository(host, port, db_name, 'value_entities')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)


class TestWork(unittest.TestCase):
    """
    Tests the Work API against a Mongo database.
    """

    def setUp(self):
        iswc = ISWCCode(12345678, 9)

        self.entity = WorkRecord(record_type='NWR',
                                 transaction_sequence_n=3,
                                 record_sequence_n=15,
                                 submitter_work_n='ABC123',
                                 title='TITLE',
                                 version_type='ORI',
                                 musical_work_distribution_category='SER',
                                 date_publication_printed_edition=datetime.datetime.strptime('20030216',
                                                                                             '%Y%m%d').date(),
                                 text_music_relationship='MTX',
                                 language_code='ES',
                                 copyright_number='ABDF146',
                                 copyright_date=datetime.datetime.strptime('20030217', '%Y%m%d').date(),
                                 music_arrangement='ORI',
                                 lyric_adaptation='MOD',
                                 excerpt_type='MOV',
                                 composite_type='MED',
                                 composite_component_count=5,
                                 iswc=iswc,
                                 work_type='BL',
                                 duration=datetime.datetime.strptime('011200', '%H%M%S').time(),
                                 catalogue_number='GGH97',
                                 opus_number='OP35',
                                 contact_id='123CONTACT',
                                 contact_name='THE CONTACT',
                                 recorded_indicator='Y',
                                 priority_flag='Y',
                                 exceptional_clause='Y',
                                 grand_rights_indicator=True)
        self.repo = MongoGenericRepository(host, port, db_name, 'works')

    def tearDown(self):
        self.repo.clear()

    def test_add(self):
        self.assertEqual(len(self.repo.get(lambda e: True)), 0)
        self.repo.add(self.entity)
        self.assertEqual(len(self.repo.get(lambda e: True)), 1)


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


if __name__ == '__main__':
    unittest.main()