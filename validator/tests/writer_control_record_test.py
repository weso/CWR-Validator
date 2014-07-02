import unittest

from validator.validator import Validator


__author__ = 'Borja'


class WriterControlValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_writer_control_record(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_writer_control_record(''))

    def test_record(self):
        self.assertTrue(self._validator.validate_writer_control_record(
            'SWR00000379000027114248028  COBAIN                                       KURT                           CA         0022707397521 02813   00000   00000    0000000000000             '))
        self.assertTrue(self._validator.validate_writer_control_record(
            'OWR00000379000027144229820  NOVOSELIC                                    KRIST                          CA         0023472039221 00469   00000   00000    0000000000000             '))

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] in ['SWR', 'OWR']:
                self.assertTrue(self._validator.validate_writer_control_record(line))