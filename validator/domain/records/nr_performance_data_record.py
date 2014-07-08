__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.cwr_utils.value_tables import TITLE_TYPES
from validator.domain.records.record import Record


class NRPerformanceDataRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'NPR')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    ARTIST_NAME = regex.get_ascii_regex(160, True)
    ARTIST_FIRST_NAME = regex.get_ascii_regex(160, True)
    ARTIST_CAE_IPI = regex.get_ascii_regex(11, True)
    ARTIST_IPI_BASE = regex.get_ascii_regex(13, True)
    LANGUAGE_CODE = regex.get_alpha_regex(2, True)
    PERFORMANCE_LANGUAGE = regex.get_alpha_regex(2, True)
    PERFORMANCE_DIALECT = regex.get_alpha_regex(3, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, ARTIST_NAME, ARTIST_FIRST_NAME, ARTIST_CAE_IPI,
        ARTIST_IPI_BASE, LANGUAGE_CODE, PERFORMANCE_LANGUAGE, PERFORMANCE_DIALECT)

    def __init__(self, record):
        super(NRPerformanceDataRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._artist_name = self.get_value(19, 160)
        self._artist_first_name = self.get_value(179, 160)
        self._artist_cae = self.get_value(339, 11)
        self._artist_ipi_base = self.get_integer_value(350, 13)
        self._language_code = self.get_value(363, 2)
        if self._language_code is not None and self._language_code not in LANGUAGE_CODES:
            raise ValueError()

        self._performance_language = self.get_value(365, 2)
        if self._performance_language is not None and self._performance_language not in LANGUAGE_CODES:
            raise ValueError()

        self._performance_dialect = self.get_value(366, 3)
        """if self._performance_dialect is not None:
            raise ValueError()"""

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()