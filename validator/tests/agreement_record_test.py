__author__ = 'Borja'
import datetime
import unittest

from validator.domain.records.agreement_record import AgreementRecord


class AGRValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            AgreementRecord(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            AgreementRecord('')

    def test_record(self):
        record = AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                N        O                00001SYN              ')

        self.assertEqual(record.attr_dict['Record prefix'].record_type, 'AGR')
        self.assertEqual(record.attr_dict['Record prefix'].transaction_number, 23)
        self.assertEqual(record.attr_dict['Record prefix'].record_number, 0)
        self.assertEqual(record.attr_dict['Submitter agreement number'], 532827921033)
        self.assertIsNone(record.attr_dict['International standard agreement number'])
        self.assertEqual(record.attr_dict['Agreement type'], 'PS')
        self.assertEqual(record.attr_dict['Agreement start date'],
                         datetime.datetime.strptime('19900801', '%Y%m%d').date())
        self.assertIsNone(record.attr_dict['Agreement end date'])
        self.assertIsNone(record.attr_dict['Retention end date'])
        self.assertEqual(record.attr_dict['Prior royalty status'], 'N')
        self.assertIsNone(record.attr_dict['Prior royalty start date'])
        self.assertEqual(record.attr_dict['Post-term collection status'], 'O')
        self.assertIsNone(record.attr_dict['Post-term collection end date'])
        self.assertIsNone(record.attr_dict['Date of signature agreement'])
        self.assertEqual(record.attr_dict['Number of works'], 1)
        self.assertEqual(record.attr_dict['Sales/Manufacture clause'], 'S')
        self.assertEqual(record.attr_dict['Shares change'], 'Y')
        self.assertEqual(record.attr_dict['Advance given'], 'N')
        self.assertIsNone(record.attr_dict['Society-assigned agreement number'])

    def test_regex_error(self):
        with self.assertRaisesRegexp(ValueError, 'REGEX ERROR:*'):
            AgreementRecord(
            'AGR0000002A0000000000532827921033              PS19900801                N        O                00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                Z        O                00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                N        O                00001SYL              ')


    def test_field_validation_error(self):
        with self.assertRaisesRegexp(ValueError, 'FIELD ERROR:*'):
            AgreementRecord(
            'ADR000000230000000000532827921033              PS19900801                N        O                00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              LL19900801                N        O                00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS199008012000010119990101N        O                00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                D        O                00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                N19900101O                00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                D19910101O                00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                N        D                00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                N        O20001212        00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS1990080120000101        N        D19990101        00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801        20000101N        D19990101        00001SYN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                N        O                00001 YN              ')
            AgreementRecord(
            'AGR000000230000000000532827921033              PS19900801                N        O                00000SYN              ')

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] == 'AGR':
                AgreementRecord(line)