__author__ = 'Borja'

import unittest
from validator.domain.records.transmission_trailer_record import TransmissionTrailer


class TRLValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            TransmissionTrailer(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            TransmissionTrailer('')

    def test_record(self):
        record = TransmissionTrailer(
            'TRL000020000053200005703')

        self.assertEqual(record.attr_dict['Record type'], 'TRL')
        self.assertEqual(record.attr_dict['Group count'], 2)
        self.assertEqual(record.attr_dict['Transaction count'], 532)
        self.assertEqual(record.attr_dict['Record count'], 5703)

    def test_regex_error(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            TransmissionTrailer(
            'TRR000020000053200005703')
            TransmissionTrailer(
            'TRL00002000005320000570A')

    def test_field_validation_error(self):
        pass