import unittest

from validator.validator import Validator


__author__ = 'Borja'


class TRLValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_transmission_trailer(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_transmission_trailer(''))

    def test_headers(self):
        self.assertTrue(self._validator.validate_transmission_trailer(
            'TRL000020000053200005703'))
        self.assertTrue(self._validator.validate_transmission_trailer(
            'trl000010000053200005703'))
        self.assertFalse(self._validator.validate_transmission_trailer(
            'rl000020000053200005703'))
