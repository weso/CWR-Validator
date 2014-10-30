import unittest

from models import regex
from models.cwr_objects import CWRField


class DocumentRegexTest(unittest.TestCase):
    def setUp(self):
        self.file_path = 'test-files/CW1328EMI_059.V21'

    def testi(self):
        field = CWRField('Title', regex.get_ascii_regex(60))
        field.value = None

        if field.value is None:
            print "Yay"
        else:
            print "do'h"
