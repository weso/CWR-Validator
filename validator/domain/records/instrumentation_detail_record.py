__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import INSTRUMENT_CODES
from validator.domain.records.record import Record


class InstrumentationDetailRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'IND')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    INSTRUMENT_CODE = regex.get_alpha_regex(3)
    PLAYERS_NUMBER = regex.get_numeric_regex(3, True)

    REGEX = "^{0}{1}{2}{3}{4}$".format(RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER,
                                       INSTRUMENT_CODE, PLAYERS_NUMBER)

    def __init__(self, record):
        super(InstrumentationDetailRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._instrument = self.get_value(19, 3)
        if self._instrument not in INSTRUMENT_CODES:
            raise ValueError()
        
        self._players = self.get_integer_value(22, 3)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()