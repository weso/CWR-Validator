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

    '''def test_agreements_groups(self):
        with open('files/valid_agreements_group') as agreements_file:
            file_content = agreements_file.readlines()

        self.assertTrue(self._validator.validate_group(file_content.pop(0), file_content))'''