__author__ = 'Borja'
import re
import xlrd


class TerritoryRecord(object):
    RECORD_TYPE = 'TER'
    AGREEMENT_ID = '\d{8}'
    RECORD_NUMBER = '\d{8}'
    EXCLUSION_INDICATOR = '[EI]'
    TIS_NUMERIC_CODE = '\d{4}'

    TERRITORY_RECORD_REGEX = "^{0}{1}{2}{3}{4}$".format(
        RECORD_TYPE, AGREEMENT_ID, RECORD_NUMBER, EXCLUSION_INDICATOR, TIS_NUMERIC_CODE)

    def __init__(self, record):
        matcher = re.compile(self.TERRITORY_RECORD_REGEX)
        if matcher.match(record.strip()):
            self._build_territory_record(record)
        else:
            raise ValueError(
                'Given record: %s does not match required format %s' % (record, self.TERRITORY_RECORD_REGEX))

    def _build_territory_record(self, record):
        self._agreement_id = int(record[3:3 + 8])
        self._excluded = True if record[19:19 + 1] == 'E' else False
        self._tis_code = record[20:20 + 4]
        if not self._check_tis_code(self._tis_code):
            raise ValueError('Given TIS code %s not recognized' % self._tis_code)

    def _check_tis_code(self, tis_code):
        codes = self._load_tis_codes()

        return int(tis_code) in codes

    @staticmethod
    def _load_tis_codes():
        codes = []
        workbook = xlrd.open_workbook('../files/TIS09-1540a_Territories_2009-08-27_EN.xls')
        worksheet = workbook.sheet_by_name('en')

        for curr_row in range(1, worksheet.nrows):
            codes.append(int(worksheet.cell_value(curr_row, 0)))

        return codes

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()