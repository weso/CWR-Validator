import unittest
from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.records.territory_record import TerritoryRecord

__author__ = 'Borja'


class TERValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
            TerritoryRecord(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
           TerritoryRecord('')

    def test_record(self):
        record = TerritoryRecord('TER0000000100000003I2136')
        self.assertEqual(record.attr_dict['Record prefix'].record_type, 'TER')
        self.assertEqual(record.attr_dict['Record prefix'].transaction_number, 1)
        self.assertEqual(record.attr_dict['Record prefix'].record_number, 3)
        self.assertEqual(record.attr_dict['Inclusion/Exclusion indicator'], 'I')
        self.assertEqual(record.attr_dict['TIS code'], 2136)

    def test_regex_error(self):
        pass

    def test_field_validation_error(self):
        with self.assertRaisesRegexp(FieldValidationError, 'record type'):
            record = TerritoryRecord('RER0000000100000003I2136')
        with self.assertRaisesRegexp(FieldValidationError, 'TIS code'):
            record = TerritoryRecord('TER0000000100000003I0000')

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0+3] == 'TER':
                TerritoryRecord(line)