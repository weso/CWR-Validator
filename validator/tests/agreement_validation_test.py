import unittest

from validator.validator import Validator


__author__ = 'Borja'


class HDRValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_agreement_record(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_agreement_record(''))

    def test_headers(self):
        self.assertTrue(self._validator.validate_agreement_record(
            'AGR000000230000000000532827921033              PS19900801                N        O                00001SYN              '))
        self.assertTrue(self._validator.validate_agreement_record(
            'AGR000000000000000000023683606100              OS200311182013111820131118N        D20131118        00009SYY              '))
        self.assertFalse(self._validator.validate_agreement_record(
            'AGR000000000000000000023683606100              RE200311182013111820131118N        D20131118        00009SYY              '))