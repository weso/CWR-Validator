__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.cwr_utils.value_tables import TITLE_TYPES
from validator.domain.record import Record


class WorkExcerptTitleRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'EWT')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    ENTIRE_WORK_TITLE = regex.get_ascii_regex(60)
    ENTIRE_WORK_ISWC = regex.get_ascii_regex(11, True)
    LANGUAGE_CODE = regex.get_alpha_regex(2, True)
    FIRST_WRITER_LAST_NAME = regex.get_ascii_regex(45, True)
    FIRST_WRITER_NAME = regex.get_ascii_regex(30, True)
    SOURCE = regex.get_ascii_regex(60, True)
    FIRST_WRITER_CAE_IPI = regex.get_numeric_regex(11, True)
    FIRST_WRITER_IPI_BASE = regex.get_numeric_regex(13, True)
    SECOND_WRITER_LAST_NAME = regex.get_ascii_regex(45, True)
    SECOND_WRITER_NAME = regex.get_ascii_regex(30, True)
    SECOND_WRITER_CAE_IPI = regex.get_numeric_regex(11, True)
    SECOND_WRITER_IPI_BASE = regex.get_numeric_regex(13, True)
    SUBMITTER_WORK_NUMBER = regex.get_ascii_regex(14, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, ENTIRE_WORK_TITLE, ENTIRE_WORK_ISWC,
        LANGUAGE_CODE, FIRST_WRITER_LAST_NAME, FIRST_WRITER_NAME, SOURCE, FIRST_WRITER_CAE_IPI,
        FIRST_WRITER_IPI_BASE, SECOND_WRITER_LAST_NAME, SECOND_WRITER_NAME, SECOND_WRITER_CAE_IPI,
        SECOND_WRITER_IPI_BASE, SUBMITTER_WORK_NUMBER)

    def __init__(self, record):
        super(WorkExcerptTitleRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._work_title = self.get_value(19, 60)
        self._work_iswc = self.get_value(79, 11)
        self._language_code = self.get_value(90, 2)
        if self._language_code is not None and self._language_code not in LANGUAGE_CODES:
            raise ValueError('')

        self._first_writer_last_name = self.get_value(92, 45)
        self._first_writer_name = self.get_value(137, 30)
        self._source = self.get_value(167, 60)
        self._first_writer_cae = self.get_integer_value(227, 11)
        self._first_writer_ipi = self.get_integer_value(238, 13)
        self._second_writer_last_name = self.get_value(251, 45)
        self._first_writer_name = self.get_value(296, 30)
        self._first_writer_cae = self.get_integer_value(326, 11)
        self._first_writer_ipi = self.get_integer_value(337, 13)
        self._work_number = self.get_integer_value(350, 14)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()