import unittest

from validator.validator import Validator


__author__ = 'Borja'


class WorkOriginValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_work_origin(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_work_origin(''))

    def test_record(self):
        self.assertTrue(self._validator.validate_work_origin(
            'ORN0000044400003579FILVALENTINA  LA PELICULA                                                     0000                                                             0000000000000000000000000            VALENTINA  LA PELICULA                                                          0000000               '))

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] == 'ORN':
                self.assertTrue(self._validator.validate_work_origin(line))