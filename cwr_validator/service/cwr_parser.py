# -*- encoding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import codecs
from random import randint
import logging

from werkzeug.utils import secure_filename
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

    @abstractmethod
    def generate_json(self, data):
        """
        Generates a JSON from the CWR model graph.

        :param data: CWR model graph to generate the JSON from
        :return: a JSON generated from the CWR model graph
        """
        raise NotImplementedError('The generate_json method must be implemented')


class ThreadingCWRParserService(CWRParserService):
    """
    Thread-based implementation of CWRParserService.

    This will generate a thread for each CWR parsing procedure, so these don't block the web service.
    """

    _logger = logging.getLogger(__name__)

    def __init__(self, path, data_service, id_service):
        super(CWRParserService, self).__init__()
        self._path = path
        self._decoder = default_file_decoder()
        self._encoder_json = JSONEncoder()

        self._data_service = data_service
        self._id_service = id_service

    def process_cwr(self, file):
        cwr_id = self._id_service.generate_id()

        file_path = os.path.join(self._path, str(cwr_id))

        # The file is temporarily saved
        file.save(file_path)

        self._parse_cwr(cwr_id, file.filename, file_path, self._decoder)

        return cwr_id

    def generate_json(self, data):
        return self._encoder_json.encode(data)

    @threaded
    def _parse_cwr(self, cwr_id, filename, file_path, decoder):
        data = {}

        data['filename'] = filename
        data['contents'] = codecs.open(file_path, 'r', 'latin-1').read()

        try:
            result = decoder.decode(data)
        except:
            result = None

        if result:
            self._data_service.store_cwr(cwr_id, result)

        os.remove(file_path)

        return result