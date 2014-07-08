__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.domain.records.record import Record


class NRSpecialTitleRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'NET', 'NCT', 'NVT')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    TITLE = regex.get_ascii_regex(640)
    LANGUAGE_CODE = regex.get_alpha_regex(2, True)

    REGEX = "^{0}{1}{2}{3}{4}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, TITLE, LANGUAGE_CODE)

    def __init__(self, record):
        super(NRSpecialTitleRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._title = self.get_value(19, 640)
        self._language_code = self.get_value(659, 2)
        if self._language_code is not None and self._language_code not in LANGUAGE_CODES:
            raise ValueError()

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()