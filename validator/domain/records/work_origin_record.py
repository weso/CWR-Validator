__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import INTENDED_PURPOSES
from validator.domain.records.record import Record
from validator.domain.values.avi_key import AviKey
from validator.domain.values.v_isan import VIsan


class WorkOriginRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'ORN')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    INTENDED_PURPOSE = regex.get_ascii_regex(3)
    PRODUCTION_TITLE = regex.get_ascii_regex(60, True)
    CD_IDENTIFIER = regex.get_ascii_regex(15, True)
    CUT_NUMBER = regex.get_numeric_regex(4, True)
    LIBRARY = regex.get_ascii_regex(60, True)
    BLT = regex.get_ascii_regex(1, True)
    V_ISAN = VIsan.REGEX
    PRODUCTION_NUMBER = regex.get_ascii_regex(12, True)
    EPISODE_TITLE = regex.get_ascii_regex(60, True)
    EPISODE_NUMBER = regex.get_ascii_regex(20, True)
    PRODUCTION_YEAR = regex.get_numeric_regex(4, True)
    AVI_KEY = AviKey.REGEX

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, INTENDED_PURPOSE, PRODUCTION_TITLE, CD_IDENTIFIER,
        CUT_NUMBER, LIBRARY, BLT, V_ISAN, PRODUCTION_NUMBER, EPISODE_TITLE, EPISODE_NUMBER, PRODUCTION_YEAR,
        AVI_KEY)

    def __init__(self, record):
        super(WorkOriginRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._intended_purpose = self.get_value(19, 3)
        if self._intended_purpose is not None and self._intended_purpose not in INTENDED_PURPOSES:
            raise ValueError()

        self._production_title = self.get_value(22, 60)
        if self._intended_purpose == 'LIB' and self._production_title is None:
            raise ValueError()

        self._cd = self.get_value(82, 15)
        if self._intended_purpose == 'LIB' and self._cd is None:
            raise ValueError()

        self._cut_number = self.get_integer_value(97, 4)
        if self._intended_purpose == 'LIB' and self._cut_number in [0, None]:
            raise ValueError()

        self._library = self.get_value(101, 60)
        if self._intended_purpose == 'LIB' and self._library is None:
            raise ValueError()

        self._blt = self.get_value(161, 1)
        self._visan = VIsan(self.get_integer_value(162, 8),
                            self.get_integer_value(170, 12),
                            self.get_integer_value(182, 4),
                            self.get_integer_value(186, 1))
        self._production_number = self.get_value(187, 12)
        self._episode_title = self.get_value(199, 60)
        self._episode_number = self.get_value(259, 20)
        self._production_year = self.get_integer_value(279, 4)
        self._avikey = AviKey(self.get_integer_value(283, 3),
                              self.get_integer_value(286, 15))

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()