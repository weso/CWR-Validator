import unittest
from validator.domain.records.group_header_record import GroupHeader

__author__ = 'Borja'


class GRPValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            GroupHeader(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            GroupHeader('')

    def test_header_record(self):
        record = GroupHeader(
            'GRHAGR0000102.100130400001  ')
        self.assertEqual(record.attr_dict['Record type'], 'GRH')
        self.assertEqual(record.attr_dict['Transaction type'], 'AGR')
        self.assertEqual(record.attr_dict['Group ID'], 1)
        self.assertEqual(record.attr_dict['Transaction type version number'], '02.10')
        self.assertEqual(record.attr_dict['Batch request'], 130400001)
        self.assertIsNone(record.attr_dict['Submission/Distribution type'])

    def test_headers(self):
        record = None
        record = GroupHeader('GRHAGR0000102.100130400001  ')
        self.assertIsNotNone(record)

        record = None
        record = GroupHeader('GRHNWR0000202.100130500002  ')
        self.assertIsNotNone(record)

        record = None
        record = GroupHeader('GRHREV0000202.100130500002  ')
        self.assertIsNotNone(record)

    def test_trailers(self):
        self.assertTrue(self._validator.validate_group_trailer(
            'GRT000010000017900000719   0000000000'))
        self.assertTrue(self._validator.validate_group_trailer(
            'grt000020000017900000719EUR0000000001'))

        # Same group id mustn't appear multiple times
        self.assertFalse(self._validator.validate_group_trailer(
            'GRT000020000017900000719   0000000000'))

        self.assertFalse(self._validator.validate_group_trailer(
            'GRT000030000017900000719   '))

        # Check why
        self.assertFalse(self._validator.validate_group_trailer(
            'GRT000030000017900000719  1111111111'))

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0+3] == 'GRT':
                self.assertTrue(self._validator.validate_group_trailer(line.rstrip()))
            elif line[0:0+3] == 'GRH':
                self.assertTrue(self._validator.validate_group_header(line))