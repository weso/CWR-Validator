__author__ = 'Borja'
import re


class GroupHeader(object):
    TRANSACTION_VALUES = {'AGR', 'NWR', 'REV'}

    RECORD_TYPE = 'GRH'
    TRANSACTION_TYPE = '([A-Z]{3})'  # Three upper case characters
    GROUP_ID = '\d{5}'
    VERSION_NUMBER = '02\.10'
    BATCH_REQUEST = '\d{10}'
    SUB_DIST_TYPE = '([ -~]{2})?'

    GROUP_HEADER_REGEX = "^{0}{1}{2}{3}{4}{5}$".format(
        RECORD_TYPE, TRANSACTION_TYPE, GROUP_ID, VERSION_NUMBER, BATCH_REQUEST, SUB_DIST_TYPE)

    def __init__(self, record):
        matcher = re.compile(self.GROUP_HEADER_REGEX)
        if matcher.match(record):
            self._build_group_header(record)
        else:
            raise ValueError('Given record: %s does not match required format' % record)

    def _build_group_header(self, record):
        self._transaction_type = record[3:3 + 3]
        if not self._transaction_type in self.TRANSACTION_VALUES:
            raise ValueError('Given transaction type: %s not in required ones' % self._transaction_type)

        self._group_id = record[6:6 + 5]
        if self._group_id > '00003':
            raise ValueError('Given group id: %s bigger than expected (00003)' % self._group_id)
        self._version_number = record[11:11 + 5]
        self._batch_request = record[16:16 + 10]

        if len(record) > 27:
            self._submission_distribution_type = record[26:26 + 2]

    @property
    def transaction_type(self):
        return self._transaction_type

    def __str__(self):
        return 'transaction type: {0}\ngroup id: {1}\nversion: {2}\nbatch request: {3}\n'\
            .format(self._transaction_type, self._group_id, self._version_number, self._batch_request)

    def __repr__(self):
        return self.__str__()