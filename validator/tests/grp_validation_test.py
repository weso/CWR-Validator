import unittest

from validator.validator import Validator


__author__ = 'Borja'


class GRPValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_group_header(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_group_header(''))

    def test_headers(self):
        self.assertTrue(self._validator.validate_group_header(
            'GRHAGR0000102.100130400001'))
        self.assertTrue(self._validator.validate_group_header(
            'GRHNWR0000202.100130500002'))
        self.assertTrue(self._validator.validate_group_header(
            'GRHREV0000202.100130500002'))

        # Same transaction group can't be validated twice
        self.assertFalse(self._validator.validate_group_header(
            'GRHAGR0000102.100130400001'))
        self.assertFalse(self._validator.validate_group_header(
            'REV0000202.100130500002'))

    def test_trailers(self):
        self.assertTrue(self._validator.validate_group_trailer(
            'GRT000010000017900000719   0000000000'))
        self.assertTrue(self._validator.validate_group_trailer(
            'grt000020000017900000719'))

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
                self.assertTrue(self._validator.validate_group_trailer(line))
            elif line[0:0+3] == 'GRH':
                self.assertTrue(self._validator.validate_group_header(line))