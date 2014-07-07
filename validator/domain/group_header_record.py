__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import TRANSACTION_VALUES
from validator.domain.record import Record


class GroupHeader(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'GRH')
    TRANSACTION_TYPE = regex.get_alpha_regex(3)
    GROUP_ID = regex.get_numeric_regex(5)
    VERSION_NUMBER = regex.get_defined_values_regex(5, False, '02\.10')
    BATCH_REQUEST = regex.get_numeric_regex(10, True)
    SUB_DIST_TYPE = regex.get_optional_regex(2)

    REGEX = "^{0}{1}{2}{3}{4}{5}$".format(
        RECORD_TYPE, TRANSACTION_TYPE, GROUP_ID, VERSION_NUMBER, BATCH_REQUEST, SUB_DIST_TYPE)

    def __init__(self, record):
        super(GroupHeader, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._transaction_type = self.get_value(3, 3)
        if not self._transaction_type in TRANSACTION_VALUES:
            raise ValueError('Given transaction type: [%s] not in required ones' % self._transaction_type)

        self._group_id = self.get_integer_value(6, 5)
        if self._group_id > len(TRANSACTION_VALUES):
            raise ValueError('Given group id: %s bigger than expected (00003)' % self._group_id)
        self._version_number = self.get_value(11, 5)
        self._batch_request = self.get_value(16, 10)

        self._submission_distribution_type = self.get_value(26, 2)

    def validate(self):
        pass

    @property
    def transaction_type(self):
        return self._transaction_type

    def __str__(self):
        return 'transaction type: {0}\ngroup id: {1}\nversion: {2}\nbatch request: {3}\n'\
            .format(self._transaction_type, self._group_id, self._version_number, self._batch_request)

    def __repr__(self):
        return self.__str__()