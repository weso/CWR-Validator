__author__ = 'Borja'
import re


class TransmissionTrailer(object):
    RECORD_TYPE = 'TRL'
    GROUP_COUNT = '\d{5}'
    TRANSACTION_COUNT = '\d{8}'
    RECORD_COUNT = '\d{8}'

    TRANSMISSION_TRAILER_REGEX = "^{0}{1}{2}{3}$".format(
        RECORD_TYPE, GROUP_COUNT, TRANSACTION_COUNT, RECORD_COUNT)

    def __init__(self, record):
        matcher = re.compile(self.TRANSMISSION_TRAILER_REGEX)
        if matcher.match(record):
            self._build_transmission_trailer(record)
        else:
            raise ValueError('Given record: %s does not match required format' % record)

    def _build_transmission_trailer(self, record):
        self._group_count = int(record[3:3 + 5])
        self._transaction_count = int(record[8:8 + 8])
        self._record_count = int(record[16:16 + 8])

    def __str__(self):
        return 'group count: {0}\ntransaction count: {1}\nrecord count: {2}\n'\
            .format(self._group_count, self._transaction_count, self._record_count)

    def __repr__(self):
        return self.__str__()