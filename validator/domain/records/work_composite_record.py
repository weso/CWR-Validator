__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.domain.records.record import Record


class WorkCompositeRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'COM')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    WORK_TITLE = regex.get_ascii_regex(60)
    COMPONENT_ISWC = regex.get_ascii_regex(11, True)
    SUBMITTER_WORK_NUMBER = regex.get_ascii_regex(14, True)
    DURATION = regex.get_time_regex(True)
    FIRST_WRITER_LAST_NAME = regex.get_ascii_regex(45)
    FIRST_WRITER_NAME = regex.get_ascii_regex(30, True)
    FIRST_WRITER_CAE_IPI = regex.get_numeric_regex(11, True)
    SECOND_WRITER_LAST_NAME = regex.get_ascii_regex(45, True)
    SECOND_WRITER_NAME = regex.get_ascii_regex(30, True)
    SECOND_WRITER_CAE_IPI = regex.get_numeric_regex(11, True)
    FIRST_WRITER_IPI_BASE = regex.get_numeric_regex(13, True)
    SECOND_WRITER_IPI_BASE = regex.get_numeric_regex(13, True)


    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, WORK_TITLE, COMPONENT_ISWC, SUBMITTER_WORK_NUMBER,
        DURATION, FIRST_WRITER_LAST_NAME, FIRST_WRITER_NAME, FIRST_WRITER_CAE_IPI, SECOND_WRITER_LAST_NAME,
        SECOND_WRITER_NAME, SECOND_WRITER_CAE_IPI, FIRST_WRITER_IPI_BASE, SECOND_WRITER_IPI_BASE)

    def __init__(self, record):
        super(WorkCompositeRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._work_title = self.get_value(19, 60)
        self._component_iswc = self.get_value(79, 11)
        self._work_number = self.get_integer_value(90, 14)
        self._duration = self.get_time_value(104, 6)
        self._first_writer_last_name = self.get_value(110, 45)
        self._first_writer_name = self.get_value(155, 30)
        self._first_writer_cae = self.get_integer_value(185, 11)
        self._second_writer_last_name = self.get_value(196, 45)
        self._second_writer_name = self.get_value(241, 30)
        self._second_writer_cae = self.get_integer_value(271, 11)
        self._first_writer_ipi = self.get_integer_value(282, 13)
        self._second_writer_ipi = self.get_integer_value(295, 13)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()