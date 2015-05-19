# -*- encoding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import codecs
from random import randint
import uuid
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

_logger = logging.getLogger(__name__)


@threaded
def _parse_cwr(filename, file_path, decoder):
    data = {}

    data['filename'] = filename
    data['contents'] = codecs.open(file_path, 'r', 'latin-1').read()

    try:
        result = decoder.decode(data)
    except:
        result = None

    os.remove(file_path)

    return result


class CWRParserService(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def process_cwr(self, file, path):
        raise NotImplementedError('The save_file method must be implemented')

    @abstractmethod
    def generate_json(self, data):
        raise NotImplementedError('The generate_json method must be implemented')


class ThreadingCWRParserService(CWRParserService):
    def __init__(self, path):
        super(CWRParserService, self).__init__()
        self._path = path
        self._decoder = default_file_decoder()
        self._encoder_json = JSONEncoder()

        self._files_data = {}

    def process_cwr(self, file, path):
        filename = '%s%s' % (secure_filename(file.filename), randint(0, 10000))
        file_path = os.path.join(path, filename)

        cwr_id = uuid.uuid4()

        # The file is temporarily saved
        file.save(file_path)

        _parse_cwr(filename, file_path, self._decoder)
        # try:
        #    _parse_cwr(filename, file_path, self._decoder)
        #except:
        #    _logger.error('Error with CWR parsing thread for id %s' % cwr_id)

        return cwr_id

    def generate_json(self, data):
        return self._encoder_json.encode(data)
