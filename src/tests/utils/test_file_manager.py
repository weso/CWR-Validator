# -*- encoding: utf-8 -*-
import os

from tests.test_files import __test_files__

"""
Offers classes to handle the access to test files in the project paths.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__version__ = '0.0.0'
__status__ = 'Development'


class FileManager(object):
    """
    Manages files in the project class path.

    Allows acquiring files from several directories, avoiding relative path issues.

    Also can save files to the uploads or validations folders.
    """

    @staticmethod
    def get_test_file(file_name):
        return os.path.join(__test_files__.path(), file_name)