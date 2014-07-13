import unittest
import datetime
from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.records.registration_record import RegistrationRecord

__author__ = 'Borja'


class REGValidationTest(unittest.TestCase):
    def test_null(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
            RegistrationRecord(None)

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, "Record can't be None"):
            RegistrationRecord('')

    def test_record(self):
        record = RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTX   ORI   ORIORI                                          N00000000000U                                                  Y')
        self.assertEqual(record.attr_dict['Record prefix'].record_type, 'NWR')
        self.assertEqual(record.attr_dict['Record prefix'].transaction_number, 179)
        self.assertEqual(record.attr_dict['Record prefix'].record_number, 0)
        self.assertEqual(record.attr_dict['Work title'], 'ESQUINA LIBERTAD')
        self.assertIsNone(record.attr_dict['Language code'])
        self.assertEqual(record.attr_dict['Submitter work ID'], '1430374')
        self.assertEqual(record.attr_dict['ISWC'], 'T0373068699')
        self.assertEqual(record.attr_dict['Copyright date'], datetime.datetime.strptime('19980730', '%Y%m%d').date())
        self.assertIsNone(record.attr_dict['Copyright number'])
        self.assertEqual(record.attr_dict['Musical work distribution category'], 'UNC')
        self.assertIsNone(record.attr_dict['Duration'])
        self.assertEqual(record.attr_dict['Recorded indicator'], 'Y')
        self.assertEqual(record.attr_dict['Text music relationship'], 'MTX')
        self.assertIsNone(record.attr_dict['Composite type'])
        self.assertEqual(record.attr_dict['Version type'], 'ORI')
        self.assertIsNone(record.attr_dict['Excerpt type'])
        self.assertEqual(record.attr_dict['Music arrangement'], 'ORI')
        self.assertEqual(record.attr_dict['Lyric adaptation'], 'ORI')
        self.assertIsNone(record.attr_dict['Contact name'])
        self.assertIsNone(record.attr_dict['Contact ID'])
        self.assertIsNone(record.attr_dict['CWR work type'])
        self.assertEqual(record.attr_dict['Grand rights indicator'], 'N')
        self.assertEqual(record.attr_dict['Composite component count'], 0)
        self.assertIsNone(record.attr_dict['Date of publication of printed edition'])
        self.assertEqual(record.attr_dict['Exceptional clause'], 'U')
        self.assertIsNone(record.attr_dict['Opus number'])
        self.assertIsNone(record.attr_dict['Catalogue number'])
        self.assertEqual(record.attr_dict['Priority flag'], 'Y')

    def test_regex_error(self):
        pass

    def test_field_validation_error(self):
        with self.assertRaisesRegexp(FieldValidationError, 'record type'):
            RegistrationRecord(
            'PER0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTX   ORI   ORIORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'language code'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                            RR1430374       T037306869919980730            UNC000000YMTX   ORI   ORIORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'distribution category'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            PPP000000YMTX   ORI   ORIORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected duration'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            SER000000YMTX   ORI   ORIORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'text music relationship'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YRRR   ORI   ORIORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'composite type'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTXSSSORI   ORIORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected component'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTXCOSORI   ORIORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'version type'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTX   RRR   ORIORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'excerpt type'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTX   ORIRRRORIORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected music arrangement'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTX   MOD      ORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'music arrangement type'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTX   MOD   SSSORI                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'Expected lyric adaptation'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTX   MOD   ORI                                             N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'lyric adaptation'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTX   MOD   ORISSS                                          N00000000000U                                                  Y')
        with self.assertRaisesRegexp(FieldValidationError, 'CWR work type'):
            RegistrationRecord(
            'NWR0000017900000000ESQUINA LIBERTAD                                              1430374       T037306869919980730            UNC000000YMTX   ORI   ORIORI                                        LLN00000000000U                                                  Y')

    def test_file(self):
        with open('files/CW1328EMI_059.V21') as cwr_file:
            file_content = cwr_file.readlines()

        for line in file_content:
            if line[0:0 + 3] in ['NWR', 'REV']:
                RegistrationRecord(line)