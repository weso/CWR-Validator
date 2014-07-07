__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.cwr_utils.value_tables import TITLE_TYPES
from validator.domain.record import Record


class WorkAlternativeTitleRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'ALT')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    ALTERNATE_TITLE = regex.get_ascii_regex(60)
    TITLE_TYPE = regex.get_alpha_regex(2)
    LANGUAGE_CODE = regex.get_alpha_regex(2, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, ALTERNATE_TITLE, TITLE_TYPE, LANGUAGE_CODE)

    def __init__(self, record):
        super(WorkAlternativeTitleRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._alternative_title = self.get_value(19, 60)
        self._title_type = self.get_value(79, 2)
        if self._title_type not in TITLE_TYPES:
            raise ValueError('Title type not in table')

        self._language_code = self.get_value(81, 2)
        if self._language_code is not None and self._language_code not in LANGUAGE_CODES:
            raise ValueError('Language code not in table')

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()