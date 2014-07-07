import unittest

from validator.validator import Validator


__author__ = 'Borja'


class WorkExcerptTitleValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_recording_detail(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_recording_detail(''))

    def test_record(self):
        pass  # Need more examples

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] == 'REC':
                self.assertTrue(self._validator.validate_recording_detail(line))