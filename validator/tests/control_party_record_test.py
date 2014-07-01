import unittest

from validator.validator import Validator


__author__ = 'Borja'


class ControlPartyValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_control_party_record(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_control_party_record(''))

    def test_record(self):
        self.assertTrue(self._validator.validate_control_party_record(
            'SPU00000179000005380166       EMI MELOGRAF SA                               E          002501650060399357851805061 0025061 0050061 00500   0000000000000                            OS '))
        self.assertTrue(self._validator.validate_control_party_record(
            'OPU0000037900002709024218832  MURKY SLOUGH MUSIC                           NE          00196070263              21 00469   00938   00938   0000000000000                            OS '))

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] in ['SPU', 'OPU']:
                self.assertTrue(self._validator.validate_control_party_record(line))