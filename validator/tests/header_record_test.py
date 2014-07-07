import unittest

from validator.validator import Validator


__author__ = 'Borja'


class HDRValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_transmission_header(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_transmission_header(''))

    def test_headers(self):
        self.assertTrue(self._validator.validate_transmission_header(
            'HDRPB226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809               '))
        self.assertTrue(self._validator.validate_transmission_header(
            'hdrPB226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809               '))
        self.assertFalse(self._validator.validate_transmission_header(
            'PB226144593EMI MUSICAL SA DE CV                         01.102013080902591120130809               '))
