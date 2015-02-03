# -*- encoding: utf-8 -*-
import os

from werkzeug.utils import secure_filename

from webapp.uploads import __uploads__
from webapp.validations import __validations__
from tests.test_files import __test_files__

"""
Offers classes to handle the access to files in the project paths.
"""

__author__ = 'Borja Garrido Bear'
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
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ['V21']

    def save_file(self, sent_file, path):
        file_folder = None

        if path == 'uploads':
            file_folder = __uploads__.path()
        elif path == 'validations':
            file_folder = __validations__.path()

        if sent_file and self.allowed_file(sent_file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(sent_file.filename)

            file_path = os.path.join(file_folder, filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            sent_file.save(file_path)

            return file_path

    @staticmethod
    def get_validations_path(file_name):
        return os.path.join(__validations__.path(), file_name)

    @staticmethod
    def get_test_file(file_name):
        return os.path.join(__test_files__.path(), file_name)