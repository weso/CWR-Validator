import unittest

from models import regex
from models.cwr_objects import CWRField


class TestSimple(unittest.TestCase):
    def setUp(self):
        self.file_path = 'test-files/CW1328EMI_059.V21'

    def test_default_value_none(self):
        field = CWRField('Title', regex.get_ascii_regex(60))
        field.value = None

        self.assertIsNone(field.value)


if __name__ == '__main__':
    unittest.main()
