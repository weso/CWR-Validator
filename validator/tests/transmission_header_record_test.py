from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.exceptions.regex_error import RegexError

__author__ = 'Borja'
import datetime
import unittest
from validator.domain.records.transmission_header_record import TransmissionHeaderRecord


class HDRValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
            TransmissionHeaderRecord(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
            TransmissionHeaderRecord('')

    def test_record(self):
        record = TransmissionHeaderRecord(
            'HDRPB226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809               ')

        self.assertEqual(record.attr_dict['Record type'], 'HDR')
        self.assertEqual(record.attr_dict['Sender type'], 'PB')
        self.assertEqual(record.attr_dict['Sender ID'], 226144593)
        self.assertEqual(record.attr_dict['Sender name'], 'EMI MUSICAL SA DE CV')
        self.assertEqual(record.attr_dict['EDI Standard version number'], '01.10')
        self.assertEqual(record.attr_dict['Creation date'], datetime.datetime.strptime('20130809', '%Y%m%d').date())
        self.assertEqual(record.attr_dict['Creation time'], datetime.datetime.strptime('025911', '%H%M%S').time())
        self.assertEqual(record.attr_dict['Transmission date'], datetime.datetime.strptime('20130809', '%Y%m%d').date())
        self.assertIsNone(record.attr_dict['Character set'])

    def test_regex_error(self):
        with self.assertRaisesRegexp(RegexError, 'Record type'):
            TransmissionHeaderRecord(
            'HDDPB226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809               ')
        with self.assertRaisesRegexp(RegexError, 'Character set'):
            TransmissionHeaderRecord(
            'HDRPB226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809')

    def test_field_validation_error(self):
        with self.assertRaisesRegexp(FieldValidationError, 'sender type'):
            TransmissionHeaderRecord(
            'HDRCC226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809               ')