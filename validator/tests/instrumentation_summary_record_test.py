import unittest

from validator.validator import Validator


__author__ = 'Borja'


class WorkOriginValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_instrumentation_summary(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_instrumentation_summary(''))

    def test_record(self):
        pass

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] == 'INS':
                self.assertTrue(self._validator.validate_instrumentation_summary(line))