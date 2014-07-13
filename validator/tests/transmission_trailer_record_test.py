from validator.domain.exceptions.regex_error import RegexError

__author__ = 'Borja'

import unittest
from validator.domain.records.transmission_trailer_record import TransmissionTrailerRecord


class TRLValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
            TransmissionTrailerRecord(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
            TransmissionTrailerRecord('')

    def test_record(self):
        record = TransmissionTrailerRecord(
            'TRL000020000053200005703')

        self.assertEqual(record.attr_dict['Record type'], 'TRL')
        self.assertEqual(record.attr_dict['Group count'], 2)
        self.assertEqual(record.attr_dict['Transaction count'], 532)
        self.assertEqual(record.attr_dict['Record count'], 5703)

    def test_regex_error(self):
        with self.assertRaisesRegexp(RegexError, 'Record type'):
            TransmissionTrailerRecord(
            'TRR000020000053200005703')
        with self.assertRaisesRegexp(RegexError, 'Record count'):
            TransmissionTrailerRecord(
            'TRL00002000005320000570A')

    def test_field_validation_error(self):
        pass