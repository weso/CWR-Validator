__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import CURRENCY_VALUES
from validator.domain.record import Record


class GroupTrailer(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'GRT')
    GROUP_ID = regex.get_numeric_regex(5)
    TRANSACTION_COUNT = regex.get_numeric_regex(8)
    RECORD_COUNT = regex.get_numeric_regex(8)

    CURRENCY = regex.get_alpha_regex(3, True)
    MONETARY_VALUE = regex.get_numeric_regex(10, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}$".format(
        RECORD_TYPE, GROUP_ID, TRANSACTION_COUNT, RECORD_COUNT, CURRENCY, MONETARY_VALUE)

    def __init__(self, record):
        super(GroupTrailer, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._group_id = self.get_value(3, 5)
        self._transaction_count = self.get_integer_value(8, 8)
        self._record_count = self.get_integer_value(16, 8)

        self._monetary_value = self.get_integer_value(27, 10)
        self._currency_indicator = self.get_value(24, 3)
        if self._monetary_value is not None and self._monetary_value > 0:
            if self._currency_indicator not in CURRENCY_VALUES:
                raise ValueError('Given currency %s indicator not in currency codes' % self._currency_indicator)

    def validate(self):
        pass

    @property
    def group_id(self):
        return self._group_id

    def __str__(self):
        return 'group id: {0}\ntransaction count: {1}\nrecord count: {2}\n'\
            .format(self._group_id, self._transaction_count, self._record_count)

    def __repr__(self):
        return self.__str__()