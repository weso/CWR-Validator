__author__ = 'Borja'
import re


class GroupTrailer(object):
    RECORD_TYPE = 'GRT'
    GROUP_ID = '\d{5}'
    TRANSACTION_COUNT = '\d{8}'
    RECORD_COUNT = '\d{8}'

    CURRENCY = '([ -~]{3}\d{10})?'

    GROUP_TRAILER_REGEX = "^{0}{1}{2}{3}{4}$".format(
        RECORD_TYPE, GROUP_ID, TRANSACTION_COUNT, RECORD_COUNT, CURRENCY)

    def __init__(self, record):
        matcher = re.compile(self.GROUP_TRAILER_REGEX)
        if matcher.match(record):
            self._build_group_trailer(record)
        else:
            raise ValueError('Given record: %s does not match required format' % record)

    def _build_group_trailer(self, record):
        self._group_id = record[3:3 + 5]
        self._transaction_count = int(record[8:8 + 8])
        self._record_count = int(record[16:16 + 8])

        if len(record) > 25:
            self._currency_indicator = record[24:24 + 3]
            self._monetary_value = float(record[27:27 + 10])

    @property
    def group_id(self):
        return self._group_id

    def __str__(self):
        return 'group id: {0}\ntransaction count: {1}\nrecord count: {2}\n'\
            .format(self._group_id, self._transaction_count, self._record_count)

    def __repr__(self):
        return self.__str__()