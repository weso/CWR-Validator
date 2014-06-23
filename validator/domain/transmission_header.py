__author__ = 'Borja'
import re
import datetime


class TransmissionHeader(object):
    SENDER_VALUES = {'PB', 'SO', 'AA', 'WR'}

    RECORD_TYPE = 'HDR'
    SENDER_TYPE = '([A-Z]{2})'  # Two upper case characters
    SENDER_ID = '\d{9}'
    SENDER_NAME = '([ -~]{45})'  # Any ASCII character 45 times
    EDI_VERSION_NUMBER = '01\.10'  # For this version this value is required
    CREATION_DATE = '\d{8}'  # Dates are in the form yyyymmdd
    CREATION_TIME = '\d{6}'  # Times are in the form hhmmss
    TRANSMISSION_DATE = '\d{8}'
    CHARACTER_SET = '([A-Z0-9 ]{15})?'  # Is an optional value

    TRANSMISSION_HEADER_REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}$".format(RECORD_TYPE, SENDER_TYPE, SENDER_ID, SENDER_NAME,
                                                                       EDI_VERSION_NUMBER, CREATION_DATE, CREATION_TIME,
                                                                       TRANSMISSION_DATE, CHARACTER_SET)

    def __init__(self, record):
        matcher = re.compile(self.TRANSMISSION_HEADER_REGEX)
        if matcher.match(record):
            self._build_transmission_header(record)
        else:
            raise ValueError('Given record: %s does not match required format' % record)

    def _build_transmission_header(self, record):
        self._sender_type = record[3:3 + 2]
        if not self._sender_type in self.SENDER_VALUES:
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