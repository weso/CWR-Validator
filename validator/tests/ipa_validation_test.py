import unittest

from validator.validator import Validator


__author__ = 'Borja'


class IPAValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_interested_party_record(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_interested_party_record(''))

    def test_headers(self):
        #  Wrong agreement type
        self.assertFalse(self._validator.validate_interested_party_record(
            'IPA0000003600000110PS0051017340400000000000004271370  VAINI MUSIC' +
            '                                                                61 0500061 1000061 10000'))

        #  Writer name in AC agreement
        self.assertFalse(self._validator.validate_interested_party_record(
            'IPA0000003600000109AC0026058307800002605828651185684  VAINIKOFF GERSGORIN' +
            '                          SERGIO DANIEL                 61 0500061 0000061 00000'))

        #  Nor share society for pr
        self.assertFalse(self._validator.validate_interested_party_record(
            'IPA0000003600000110AC0051017340400000000000004271370  VAINI MUSIC' +
            '                                                                   0500061 1000061 10000'))

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] == 'IPA':
                self.assertTrue(self._validator.validate_interested_party_record(line))