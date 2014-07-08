__author__ = 'Borja'
import datetime

from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import SENDER_VALUES
from validator.domain.records.record import Record


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
        self._sender_type = self.get_value(3, 2)
        if not self._sender_type in SENDER_VALUES:
            raise ValueError('Given sender type: %s not in required ones' % self._sender_type)

        self._sender_id = self.get_integer_value(5, 9)
        self._sender_name = self.get_value(14, 45)
        self._creation_date = datetime.datetime.combine(self.get_date_value(64, 8), self.get_time_value(72, 6))
        self._transmission_date = self.get_date_value(78, 8)
        self._character_field = self.get_value(85, 15)

    def validate(self):
        pass

    def __str__(self):
        return 'sender type: {0}\nsender id: {1}\nsender name: {2}\ncreation date: {3}\ntransmission date: {4}\n' \
            .format(self._sender_type, self._sender_id, self._sender_name, self._creation_date, self._transmission_date)

    def __repr__(self):
        return self.__str__()