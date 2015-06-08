# -*- encoding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import codecs
import logging
import sys
import json
import requests
from requests import ConnectionError

from cwr.parser.decoder.file import default_file_decoder
from cwr.parser.encoder.cwrjson import JSONEncoder

from cwr_validator.util.parallel import threaded

"""
Services for parsing CWR files.

These allow creating the model graph from a CWR file, but also transforming it to and from JSON messages.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class CWRParserService(object):
    """
    Service for parsing CWR files and model instances.

    It can transform a CWR file into a graph of model classes, and can generate a JSON from such a graph.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def process_cwr(self, file):
        """
        Transforms a CWR file into a graph of model classes.

        As processing the file can take a long time, this method will return an unique identifier for the file being
        parsed.

        This ID can be used to check the parsing status of the file.

        :param file: the CWR file to parse
        :return: an unique ID for the file
        """
        raise NotImplementedError('The save_file method must be implemented')


class ThreadingCWRParserService(CWRParserService):
    """
    Thread-based implementation of CWRParserService.

    This will generate a thread for each CWR parsing procedure, so these don't block the web service.
    """

    _logger = logging.getLogger(__name__)

    def __init__(self, path, id_service):
        super(CWRParserService, self).__init__()
        self._path = path
        self._decoder = default_file_decoder()
        self._encoder_json = JSONEncoder()

        self._id_service = id_service

    def process_cwr(self, file):
        cwr_id = self._id_service.generate_id()

        file_path = os.path.join(self._path, str(cwr_id))

        # The file is temporarily saved
        with open(file_path, 'w') as f:
            contents = file['contents']

            if sys.version_info[0] > 2:
                # For Python 3
                contents = str(contents)

            f.write(contents.encode("UTF-8"))

        self._parse_cwr_threaded(cwr_id, file.filename, file_path)

        return cwr_id

    @threaded
    def _parse_cwr_threaded(self, cwr_id, filename, file_path):
        self.parse_cwr(cwr_id, filename, file_path)

    def parse_cwr(self, cwr_id, filename, file_path):
        data = {}

        data['filename'] = filename
        data['contents'] = codecs.open(file_path, 'r', 'latin-1').read()

        try:
            result = self._decoder.decode(data)
        except:
            result = None

        if result:
            self._send_results(cwr_id, self._encoder_json.encode(result))

        os.remove(file_path)

    def _send_results(self, cwr_id, result):
        # TODO: Do this in a cleaner way

        headers = {'Content-Type': 'application/json'}

        data = {
            'id':str(cwr_id),
            'data':result
        }

        try:
            requests.post('http://127.0.0.1:33567/files/', data=json.dumps(data), headers=headers)
        except ConnectionError:
            self._logger.error('Failure when sending results')
