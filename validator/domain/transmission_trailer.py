__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.domain.record import Record


class TransmissionTrailer(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'TRL')
    GROUP_COUNT = regex.get_numeric_regex(5)
    TRANSACTION_COUNT = regex.get_numeric_regex(8)
    RECORD_COUNT = regex.get_numeric_regex(8)

    REGEX = "^{0}{1}{2}{3}$".format(
        RECORD_TYPE, GROUP_COUNT, TRANSACTION_COUNT, RECORD_COUNT)

    def __init__(self, record):
        super(TransmissionTrailer, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._group_count = self.get_integer_value(3, 5)
        self._transaction_count = self.get_integer_value(8, 8)
        self._record_count = self.get_integer_value(16, 8)

    def validate(self):
        pass
    
    def __str__(self):
        return 'group count: {0}\ntransaction count: {1}\nrecord count: {2}\n'\
            .format(self._group_count, self._transaction_count, self._record_count)

    def __repr__(self):
        return self.__str__()