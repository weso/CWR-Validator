import unittest

from validator.validator import Validator


__author__ = 'Borja'


class WriterAgentValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_performing_artist_record(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_performing_artist_record(''))

    def test_record(self):
        self.assertTrue(self._validator.validate_performing_artist_record(
            'PER0000018800000623SERGIO VAINIKOFF                                                           000000000000000000000000'))

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] == 'PER':
                self.assertTrue(self._validator.validate_performing_artist_record(line))