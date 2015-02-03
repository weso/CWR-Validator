from __future__ import absolute_import
from __future__ import unicode_literals
import codecs
import unittest

from validator import Validator
from utils.file_manager import FileManager


__author__ = 'Borja'


class TestRecords(unittest.TestCase):
    def test_wrong_records(self):
        validator = Validator()

        records = [
            'HDRPB226144593EMI MUSICAL SA DE CV                         01.10201308090259112013080A               ',
            'GRHAGD0000102.100130400001  ',
            'TER0000000000000000J2136'
        ]

        valid_record, invalid_records = validator.validate_document_format(records)

        self.assertEqual(0, len(valid_record))
        self.assertEqual(len(records), len(invalid_records))


class TestFile(unittest.TestCase):
    def setUp(self):
        file_manager = FileManager()
        self.file_path = file_manager.get_test_file("CW1328EMI_059.V21")

    def test_file(self):
        validator = Validator()

        with codecs.open(self.file_path, encoding='utf-8') as file_utf8:
            document_content = file_utf8.readlines()

            valid_records, invalid_records = validator.validate_document_format(document_content)

        self.assertNotEqual(len(valid_records), 0)
        self.assertEqual(len(invalid_records), 0)
        self.assertEqual(len(document_content), len(valid_records))

        validator.validate_document_structure()

        with open('CWROutput.V21', "w") as output_file:
            for record in sorted(validator.document.extract_records(), key=lambda item: item.number):
                output_file.write((record._record + "\n").encode('utf-8'))
                for message in record.messages:
                    output_file.write(str(message) + "\n")


if __name__ == '__main__':
    unittest.main()
