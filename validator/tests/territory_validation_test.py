import unittest

from validator.validator import Validator


__author__ = 'Borja'


class TERValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_territory_record(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_territory_record(''))

    def test_headers(self):
        self.assertTrue(self._validator.validate_territory_record(
            'TER0000000100000003I2136'))
        self.assertTrue(self._validator.validate_territory_record(
            'TER0000000300000009E0484'))
        self.assertFalse(self._validator.validate_territory_record(
            'TER0000000300000009F0484'))
        self.assertFalse(self._validator.validate_territory_record(
            'TER0000000300000009E484'))

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0+3] == 'TER':
                self.assertTrue(self._validator.validate_territory_record(line))