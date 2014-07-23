import re
from domain.document import Document
from domain.exceptions.regex_error import RegexError

__author__ = 'Borja'


class Validator(object):
    NAME_REGEX = '^CW\d{2}\d{4}([A-Za-z_0-9]{6})\.V\d{2}$'
    PREV_VERSION_NAME_REGEX = '^CW\d{2}\d{2}([A-Za-z_0-9]{7})\.V\d{2}$'

    def __init__(self):
        self._document = None

    def run(self, file_path):
        file_name = self._extract_name(file_path)
        if self._validate_name(file_name):
            print 'Validating file...'
            self._validate_file(file_path, file_name)
            print 'File validated'
        else:
            raise RegexError('File name', self.NAME_REGEX, file_name)

    def _validate_file(self, file_path, file_name):
        self._document = Document(file_name)
        with open(file_path) as file:
            content = file.readlines()

        for line in content:
            self._document.add_record(line)

    def _validate_name(self, file_name):
        if file_name is None:
            return False

        matcher = re.compile(self.NAME_REGEX)
        if not matcher.match(file_name.upper()):
            matcher = re.compile(self.PREV_VERSION_NAME_REGEX)
            if matcher.match(file_name.upper()):
                print 'CWR file is in a previous file name convention'
                return True
            return False

        return True

    def _extract_name(self, file_path):
        if '/' in file_path:
            file_name = file_path.rsplit('/', 1)[1]
        else:
            file_name = file_path.rsplit('\\', 1)[1]

        return file_name

    @property
    def document(self):
        return self._document