# -*- coding: utf-8 -*-

import unittest

from cwr_validator import create_app

from flask.ext.testing import TestCase


__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class TestReceive(unittest.TestCase):
    def setUp(self):
        self._app = create_app()

        self._app.config['DEBUG'] = False
        self._app.config['TESTING'] = True

        self._client = self._app.test_client()

    def test_post_no_file(self):
        response = self._client.post('/upload/')
        self.assertEqual(response.status_code, 405)