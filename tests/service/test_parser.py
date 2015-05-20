# -*- encoding: utf-8 -*-

import unittest

from cwr_validator.service.cwr_parser import ThreadingCWRParserService
from cwr_validator.service.data import MemoryDataStoreService
from cwr_validator.service.identifier import UUIDIdentifierService
from cwr_validator.uploads import __uploads__
from tests.data import __data_test__


__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class TestUpload(unittest.TestCase):
    def setUp(self):
        self._path_test = __data_test__.path()
        path = __uploads__.path()
        data = MemoryDataStoreService()
        identifier = UUIDIdentifierService()
        self._parser = ThreadingCWRParserService(path, data, identifier)


    def test_parse_invalid(self):
        file_path = '%s/test_parse_invalid' % self._path_test

        file = open(file_path, 'wb')
        file.write('')
        file.close()

        result = self._parser.parse_cwr(0, 'empty.txt', file_path)

        self.assertEqual(None, result)