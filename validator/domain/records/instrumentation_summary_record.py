__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import INSTRUMENTATION_CODES
from validator.domain.records.record import Record


class InstrumentationSummaryRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'INS')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    VOICES_NUMBER = regex.get_numeric_regex(3, True)
    INSTRUMENTATION_TYPE = regex.get_ascii_regex(3, True)
    INSTRUMENTATION_DESCRIPTION = regex.get_ascii_regex(50, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}$".format(RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER,
                                          VOICES_NUMBER, INSTRUMENTATION_TYPE, INSTRUMENTATION_DESCRIPTION)

    def __init__(self, record):
        super(InstrumentationSummaryRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._voices_number = self.get_integer_value(19, 3)
        self._instrumentation_type = self.get_value(22, 3)
        if self._instrumentation_type is not None and self._instrumentation_type not in INSTRUMENTATION_CODES:
            raise ValueError()
        
        self._instrumentation_description = self.get_value(25, 50)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()