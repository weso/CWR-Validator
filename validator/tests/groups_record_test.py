import unittest
from validator.domain.records.group_header_record import GroupHeaderRecord
from validator.domain.records.group_trailer_record import GroupTrailerRecord

__author__ = 'Borja'


class GRPValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            GroupHeaderRecord(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            GroupHeaderRecord('')

    def test_header_record(self):
        record = GroupHeaderRecord(
            'GRHAGR0000102.100130400001  ')
        self.assertEqual(record.attr_dict['Record type'], 'GRH')
        self.assertEqual(record.attr_dict['Transaction type'], 'AGR')
        self.assertEqual(record.attr_dict['Group ID'], 1)
        self.assertEqual(record.attr_dict['Transaction type version number'], '02.10')
        self.assertEqual(record.attr_dict['Batch request'], 130400001)
        self.assertIsNone(record.attr_dict['Submission/Distribution type'])

    def test_headers(self):
        record = None
        record = GroupHeaderRecord('GRHAGR0000102.100130400001  ')
        self.assertIsNotNone(record)

        record = None
        record = GroupHeaderRecord('GRHNWR0000202.100130500002  ')
        self.assertIsNotNone(record)

        record = None
        record = GroupHeaderRecord('GRHREV0000202.100130500002  ')
        self.assertIsNotNone(record)

    def test_trailer_record(self):
        record = GroupTrailerRecord('GRT000010000017900000719   0000000000')
        self.assertEqual(record.attr_dict['Record type'], 'GRT')
        self.assertEqual(record.attr_dict['Group ID'], 1)
        self.assertEqual(record.attr_dict['Transaction count'], 179)
        self.assertEqual(record.attr_dict['Record count'], 719)
        self.assertIsNone(record.attr_dict['Currency indicator'])
        self.assertEqual(record.attr_dict['Total monetary value'], 0)

    def test_regex_error(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            GroupHeaderRecord('GRPREV0000202.100130500002  ')
            GroupTrailerRecord('GRR000010000017900000719   0000000000')

    def test_field_validation_error(self):
        with self.assertRaisesRegexp(ValueError, 'FIELD ERROR:*'):
            GroupHeaderRecord('GRHPPP0000202.100130500002  ')
            GroupHeaderRecord('GRHREV0000502.100130500002  ')

            GroupTrailerRecord('GRR000010000017900000719   0000000001')
            GroupTrailerRecord('GRR000010000017900000719ABC0000000001')

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0+3] == 'GRH':
                GroupHeaderRecord(line)
            elif line[0:0+3] == 'GRT':
                GroupTrailerRecord(line)