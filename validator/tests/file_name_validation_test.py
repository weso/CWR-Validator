import unittest

from validator.validator import Validator


__author__ = 'Borja'


class NameValidationTest(unittest.TestCase):

    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_name(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_name(''))

    def test_format(self):
        self.assertTrue(self._validator.validate_name('CW901234111aaa.V21'))
        self.assertTrue(self._validator.validate_name('cw901234111aaa.v21'))
        self.assertTrue(self._validator.validate_name('CW901234aaaaa1.V21'))

        self.assertFalse(self._validator.validate_name('CW9012aaaaa1.V21'))

        self.assertFalse(self._validator.validate_name('CW9a1234111aaa.V21'))
        self.assertFalse(self._validator.validate_name('CW901234aa.aaa.V21'))
        self.assertFalse(self._validator.validate_name('CW901234111aaa.V2x'))
        self.assertFalse(self._validator.validate_name('CW90123411aaa.V2x'))