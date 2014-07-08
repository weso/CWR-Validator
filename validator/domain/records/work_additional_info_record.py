__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import RIGHT_TYPES
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.cwr_utils.value_tables import SUBJECT_CODES
from validator.domain.records.record import Record


class WorkAdditionalInfoRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'ARI')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    SOCIETY_NUMBER = regex.get_numeric_regex(3)
    WORK_NUMBER = regex.get_ascii_regex(14, True)
    RIGHT_TYPE = regex.get_alpha_regex(3)
    SUBJECT_CODE = regex.get_alpha_regex(2, True)
    NOTE = regex.get_ascii_regex(160, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, SOCIETY_NUMBER, WORK_NUMBER, RIGHT_TYPE,
        SUBJECT_CODE, NOTE)

    def __init__(self, record):
        super(WorkAdditionalInfoRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._society_id = self.get_integer_value(19, 3)
        if self._society_id not in SOCIETY_CODES:
            raise ValueError()

        self._work_id = self.get_value(22, 14)
        self._right_types = self.get_value(36, 3)
        if self._right_types not in RIGHT_TYPES:
            raise ValueError()

        self._subject = self.get_value(39, 2)
        self._info = self.get_value(41, 160)
        if self._info is not None and self._subject not in SUBJECT_CODES:
            raise ValueError()

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()