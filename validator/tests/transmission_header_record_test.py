__author__ = 'Borja'
import datetime
import unittest
from validator.domain.records.transmission_header_record import TransmissionHeader


class HDRValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            TransmissionHeader(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            TransmissionHeader('')

    def test_record(self):
        header = TransmissionHeader(
            'HDRPB226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809               ')

        self.assertEqual(header.attr_dict['Record type'], 'HDR')
        self.assertEqual(header.attr_dict['Sender type'], 'PB')
        self.assertEqual(header.attr_dict['Sender ID'], 226144593)
        self.assertEqual(header.attr_dict['Sender name'], 'EMI MUSICAL SA DE CV')
        self.assertEqual(header.attr_dict['EDI Standard version number'], '01.10')
        self.assertEqual(header.attr_dict['Creation date'], datetime.datetime.strptime('20130809', '%Y%m%d').date())
        self.assertEqual(header.attr_dict['Creation time'], datetime.datetime.strptime('025911', '%H%M%S').time())
        self.assertEqual(header.attr_dict['Transmission date'], datetime.datetime.strptime('20130809', '%Y%m%d').date())
        self.assertIsNone(header.attr_dict['Character set'])

    def test_regex_error(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            TransmissionHeader(
            'HDDPB226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809               ')
            TransmissionHeader(
            'HDRPB226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809')

    def test_field_validation_error(self):
        with self.assertRaisesRegexp(ValueError, 'FIELD ERROR:*'):
            TransmissionHeader(
            'HDRCC226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809               ')