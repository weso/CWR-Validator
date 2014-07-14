import unittest
from validator.domain.exceptions.field_validation_error import FieldValidationError

from validator.domain.records.interested_party_record import InterestedPartyRecord

__author__ = 'Borja'


class IPAValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
            InterestedPartyRecord(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
            InterestedPartyRecord('')

    def test_record(self):
        record = InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  000004  000004  00000')
        self.assertEqual(record.attr_dict['Record prefix'].record_type, 'IPA')
        self.assertEqual(record.attr_dict['Record prefix'].transaction_number, 177)
        self.assertEqual(record.attr_dict['Record prefix'].record_number, 533)
        self.assertEqual(record.attr_dict['Agreement role code'], 'AS')
        self.assertEqual(record.attr_dict['Interested party CAE/IPI ID'], 672285232)
        self.assertEqual(record.attr_dict['IPI base number'], 0)
        self.assertEqual(record.attr_dict['Interested party ID'], '4316979')
        self.assertEqual(record.attr_dict['Interested party last name'], 'REFUGIO CANCIONERO SRL')
        self.assertIsNone(record.attr_dict['Interested party writer first name'])
        self.assertEqual(record.attr_dict['PR affiliation society'], 4)
        self.assertEqual(record.attr_dict['PR share'], 0)
        self.assertEqual(record.attr_dict['MR affiliation society'], 4)
        self.assertEqual(record.attr_dict['MR share'], 0)
        self.assertEqual(record.attr_dict['SR affiliation society'], 4)
        self.assertEqual(record.attr_dict['SR share'], 0)

    def test_regex_error(self):
        pass

    def test_field_validation_error(self):
        with self.assertRaisesRegexp(FieldValidationError, 'record type'):
            InterestedPartyRecord('API0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  000004  000004  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'agreement role code'):
            InterestedPartyRecord('IPA0000017700000533TT0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  000004  000004  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'writer first name'):
            InterestedPartyRecord('IPA0000017700000533AC0067228523200000000000004316979  REFUGIO CANCIONERO SRL                       WRITERNAME                    4  000004  000004  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'PR society'):
            InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     0  000004  000004  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'MR society'):
            InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  000000  000004  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'SR society'):
            InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  000004  000000  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected PR share'):
            InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  100014  000004  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected MR share'):
            InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  000004  100014  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected SR share'):
            InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  000004  000004  10001')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected PR society'):
            InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                        100004  000004  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected MR society'):
            InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  00000   100004  00000')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected SR society'):
            InterestedPartyRecord('IPA0000017700000533AS0067228523200000000000004316979  REFUGIO CANCIONERO SRL                                                     4  000004  00000   10000')

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0+3] == 'IPA':
                InterestedPartyRecord(line)