# -*- encoding: utf-8 -*-
import os
import codecs

from werkzeug.utils import secure_filename
from cwr.parser.file import CWRFileDecoder
import chardet

from cwr_validator.uploads import __uploads__


"""
Offers classes to handle the access to files in the project paths.
"""

__author__ = 'Borja Garrido Bear, Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class FileManager(object):
    """
    Manages files in the project class path.

    Allows acquiring files from several directories, avoiding relative path issues.

    Also can save files to the uploads or validations folders.
    """

    @staticmethod
    def save_file_cwr(sent_file):
        FileManager._save_file(sent_file, __uploads__.path())

    @staticmethod
    def _save_file(sent_file, path):

        if sent_file:
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(sent_file.filename)

            file_path = os.path.join(path, filename)
            # Move the file from the temporal folder to
            # the upload folder we setup
            sent_file.save(file_path)

    @staticmethod
    def read_cwr(filename):
        decoder = CWRFileDecoder()
        file_path = os.path.join(__uploads__.path(), filename)
        return decoder.decode(file_path)

    @staticmethod
    def _read(path):
        read_file = open(path, 'rt')

        rawdata = read_file.readline()
        result = chardet.detect(rawdata)
        charenc = result['encoding']

        read_file = codecs.open(path, 'r', 'latin-1')
        file = read_file.readline()

        if charenc == 'UTF-8-SIG':
            file = file[3:]

        for line in read_file:
            file += line

        return file