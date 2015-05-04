# -*- encoding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from webapp.utils.file_manager import FileManager


"""
Offers services for CWR files.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class CWRFileService(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_data(self, id):
        pass

    @abstractmethod
    def save_file(self, file):
        pass

    @abstractmethod
    def process_file(self, id):
        pass


class LocalCWRFileService(CWRFileService):
    def __init__(self):
        super(LocalCWRFileService, self).__init__()
        self._fileManager = FileManager
        self._files_data = {}

    def get_data(self, id):
        if id in self._files_data:
            data = self._files_data[id]
        else:
            data = self._fileManager.read_cwr(id)
            self._files_data[id] = data

        return data

    def save_file(self, file):
        self._fileManager.save_file_cwr(file)

        return file.filename

    def process_file(self, id):
        if not id in self._files_data:
            data = self._fileManager.read_cwr(id)
            self._files_data[id] = data