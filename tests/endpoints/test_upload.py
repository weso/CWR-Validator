# -*- coding: utf-8 -*-

import unittest
from json import JSONEncoder
import json

from cwr_validator import create_app

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class TestUpload(unittest.TestCase):
    def setUp(self):
        self._app = create_app()

        self._app.config['DEBUG'] = False
        self._app.config['TESTING'] = True

        self._client = self._app.test_client()

    def test_get(self):
        response = self._client.get('/upload/')
        self.assertEqual(response.status_code, 200)

    def test_post_no_file(self):
        response = self._client.post('/upload/',
                                     headers={
                                         'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_post_file_with_invalid_data(self):
        json_data = JSONEncoder().encode(
            {
                'file_id': '123',
                'filename': 'hello_world.txt',
                'contents': 'my file contents'
            }
        )

        response = self._client.post('/upload/', data=json_data,
                                     headers={
                                         'content-type': 'application/json'})

        self.assertEqual(response.status_code, 200)

        data = json.loads(str(response.data))

        self.assertTrue('id' in data)

    def test_post_file_with_valid_data(self):
        json_data = JSONEncoder().encode(
            {
                'file_id': '123',
                'filename': 'hello_world.txt',
                'contents': _file_contents_cwr()
            }
        )

        response = self._client.post('/upload/', data=json_data,
                                     headers={
                                         'content-type': 'application/json'})

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertTrue('id' in data)


def _file_contents_cwr():
    header_file = 'HDRPB226144593AGENCIA GRUPO MUSICAL                        01.102013080902591120130809               '
    header_group1 = 'GRHAGR0000102.100130400001  '
    agr = 'AGR000000000000000000023683606100              OS200311182013111820131118N        D20131118        00009SYY              '
    territory = 'TER0000000000000000I2136'
    ipa_1 = 'IPA0000000000000001AS0026166137500000000000001183606  ITALIAN                                      GILBERTI DUANTE               61 0500061 0000061 00000'
    ipa_2 = 'IPA0000000000000002AC00250165006000000000000066       SOCIETY MUSIC                                                              61 0500061 1000061 10000'
    trailer_group1 = 'GRT000010000017900000719   0000000000'
    trailer_file = 'TRL000020000053200005703'

    transaction1 = agr + '\n' + territory + '\n' + ipa_1 + '\n' + ipa_2

    transaction2 = 'NWR0000019900000000WORK NAME                                                     1450455                  00000000            UNC000000YMTX   ORI   ORIORI                                          N00000000000U                                                  Y' + '\n' + \
                   'SPU0000019900000702014271370  MUSIC SOCIETY                                 E          005101734040102328568410061 0500061 1000061 10000   0000000000000                            OS ' + '\n' + \
                   'SPU00000199000007030166       ANOTHER SOCIETY                               AM         002501650060477617137010061 0000061 0000061 00000   0000000000000                            PS ' + '\n' + \
                   'SPU00000199000007040170       YET ANOTHER SOCIETY                           SE         002261445930035870006610059 00000   00000   00000   0000000000000                            PG ' + '\n' + \
                   'SPT000001990000070570             050000500005000I0484Y001' + '\n' + \
                   'SWR00000199000007061185684  A NAME                                       YET ANOTHER NAME               C          0026058307861 0500061 0000061 00000    0000260582865             ' + '\n' + \
                   'SWT00000199000007071185684  050000500005000I0484Y001' + '\n' + \
                   'PWR00000199000007084271370  MUSIC SOCIETY                                01023285684100              1185684  ' + '\n' + \
                   'PER0000019900000709A NAME                                                                     000000000000000000000000' + '\n' + \
                   'REC000001990000071019980101                                                            000300     A COMPILATION                                               P A I  _AR_                                                 33002                                       U   '

    header_group2 = 'GRHNWR0000102.100130400001  '
    trailer_group2 = 'GRT000010000017900000719   0000000000'

    record = header_file + '\n' + \
             header_group1 + '\n' + \
             transaction1 + '\n' + \
             transaction1 + '\n' + \
             trailer_group1 + '\n' + \
             header_group2 + '\n' + \
             transaction2 + '\n' + \
             transaction2 + '\n' + \
             trailer_group2 + '\n' + \
             trailer_file

    return record
