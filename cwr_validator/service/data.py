# -*- encoding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import logging


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

    @abstractmethod
    def get_cwr(self, cwr_id):
        raise NotImplementedError('The save_file method must be implemented')


class MemoryDataStoreService(DataStoreService):
    def __init__(self):
        super(MemoryDataStoreService, self).__init__()
        self._cwr_dict = {}

    def store_cwr(self, cwr_id, cwr_data):
        self._cwr_dict[cwr_id] = cwr_data

    def get_cwr(self, cwr_id):
        if cwr_id in self._cwr_dict:
            result = self._cwr_dict[cwr_id]
        else:
            result = None

        return result