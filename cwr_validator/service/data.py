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
Services for storing CWR files data.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'

_logger = logging.getLogger(__name__)


class DataStoreService(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def store_cwr(self, cwr_id, cwr_data):
        raise NotImplementedError('The save_file method must be implemented')


class MemoryDataStoreService(DataStoreService):

    def __init__(self):
        super(MemoryDataStoreService, self).__init__()
        self._cwr_dict = {}

    def store_cwr(self, cwr_id, cwr_data):
        self._cwr_dict[cwr_id] = cwr_data