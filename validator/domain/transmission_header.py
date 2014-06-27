__author__ = 'Borja'
import datetime

from validator.cwr_regex import regex
from validator.cwr_regex.value_tables import SENDER_VALUES
from validator.domain.record import Record


class TransmissionHeader(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'HDR')
    SENDER_TYPE = regex.get_alpha_regex(2)
    SENDER_ID = regex.get_numeric_regex(9)
    SENDER_NAME = regex.get_ascii_regex(45)
    EDI_VERSION_NUMBER = regex.get_defined_values_regex(5, False, '01\.10')  # For this version this value is required
    CREATION_DATE = regex.get_date_regex()
    CREATION_TIME = regex.get_time_regex()
    TRANSMISSION_DATE = regex.get_date_regex()
    CHARACTER_SET = regex.get_alphanumeric_regex(15, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}$".format(RECORD_TYPE, SENDER_TYPE, SENDER_ID, SENDER_NAME,
                                                   EDI_VERSION_NUMBER, CREATION_DATE, CREATION_TIME,
                                                   TRANSMISSION_DATE, CHARACTER_SET)

    def __init__(self, record):
        super(TransmissionHeader, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._sender_type = record[3:3 + 2]
        if not self._sender_type in SENDER_VALUES:
            raise ValueError('Given sender type: %s not in required ones' % self._sender_type)

        self._sender_id = int(record[5:5 + 9])
        self._sender_name = record[14:14 + 45]
        self._creation_date = datetime.datetime.strptime(record[64:64 + 8] + record[72:72 + 6], '%Y%m%d%H%M%S')
        self._transmission_date = datetime.datetime.strptime(record[78:78 + 8], '%Y%m%d').date()

        if len(record) > 87:
            self._character_field = record[86:86 + 15]

    def __str__(self):
        return 'sender type: {0}\nsender id: {1}\nsender name: {2}\ncreation date: {3}\ntransmission date: {4}\n' \
            .format(self._sender_type, self._sender_id, self._sender_name, self._creation_date, self._transmission_date)

    def __repr__(self):
        return self.__str__()