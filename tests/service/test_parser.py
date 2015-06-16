# -*- encoding: utf-8 -*-

import unittest
import codecs

from cwr_validator.service import ThreadingCWRParserService
from cwr_validator.uploads import __uploads__
from tests.data import __data_test__

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class TestUpload(unittest.TestCase):
    def setUp(self):
        self._path_test = __data_test__.path()
        path = __uploads__.path()
        self._parser = ThreadingCWRParserService(path, 'http://127.0.0.1/')

    def test_parse_invalid(self):
        file_path = '%s/test_parse_invalid' % self._path_test

        file = codecs.open(file_path, 'w')
        file.write('')
        file.close()

        result = self._parser.parse_cwr(0, 'empty.txt', file_path)

        self.assertEqual(None, result)
