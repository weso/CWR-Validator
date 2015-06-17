# -*- coding: utf-8 -*-

import os

"""
Facades for accessing the configuration data.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class _FileReader(object):
    """
    Offers methods to read the data files.
    """

    # Singleton control object
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __path(self):
        """
        Returns the path to the folder in which this class is contained.

        As this class is to be on the same folder as the data files, this will be the data files folder.

        :return: path to the data files folder.
        """
        return os.path.dirname(__file__)

    def read_properties(self, file_name):
        config = {}
        with open(os.path.join(self.__path(), os.path.basename(file_name)),
                  'rt') as f:
            for line in f:
                line = line.rstrip()  # removes trailing whitespace and '\n' chars

                if "=" not in line: continue  # skips blanks and comments w/o =
                if line.startswith(
                    "#"): continue  # skips comments which contain =

                k, v = line.split("=", 1)
                config[k] = v

        return config


class CWRValidatorConfiguration(object):
    """
    Offers methods to access the CWR web application configuration data.
    """

    def __init__(self):
        # Reader for the files
        self._reader = _FileReader()

        # Files containing the CWR info
        self._file_config = 'config.properties'

        # Configuration
        self._config = None

    def get_config(self):
        """
        Loads the configuration file.

        :return: the webapp configuration
        """
        if not self._config:
            self._config = self._reader.read_properties(self._file_config)

        return self._config
