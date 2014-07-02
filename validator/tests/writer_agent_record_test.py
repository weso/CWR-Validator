import unittest

from validator.validator import Validator


__author__ = 'Borja'


class WriterAgentValidationTest(unittest.TestCase):
    def setUp(self):
        self._validator = Validator()

    def test_null(self):
        self.assertFalse(self._validator.validate_writer_agent_record(None))

    def test_empty(self):
        self.assertFalse(self._validator.validate_writer_agent_record(''))

    def test_record(self):
        self.assertTrue(self._validator.validate_writer_agent_record(
            'PWR00000189000006314271370  VAINI MUSIC                                  01023285684100              1185684  '))

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] == 'PWR':
                self.assertTrue(self._validator.validate_writer_agent_record(line))