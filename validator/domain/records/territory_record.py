__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import TIS_CODES
from validator.domain.records.record import Record


class TerritoryRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'TER')
    AGREEMENT_ID = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    EXCLUSION_INDICATOR = regex.get_defined_values_regex(1, False, 'E', 'I')
    TIS_NUMERIC_CODE = regex.get_numeric_regex(4)

    REGEX = "^{0}{1}{2}{3}{4}$".format(
        RECORD_TYPE, AGREEMENT_ID, RECORD_NUMBER, EXCLUSION_INDICATOR, TIS_NUMERIC_CODE)

    def __init__(self, record):
        super(TerritoryRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._agreement_id = self.get_integer_value(3, 8)
        self._excluded = self.get_value(19, 1) == 'E'
        self._tis_code = self.get_integer_value(20, 4)
        if self._tis_code not in TIS_CODES:
            raise ValueError('Given TIS code %s not recognized' % self._tis_code)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()