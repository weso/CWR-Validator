__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.domain.record import Record


class WriterAgentRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'PWR')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    PUBLISHER_IP_NUMBER = regex.get_ascii_regex(9)
    PUBLISHER_NAME = regex.get_ascii_regex(45)
    SUBMITTER_AGREEMENT_NUMBER = regex.get_ascii_regex(14, True)
    SOCIETY_ASSIGNED_AGREEMENT_NUMBER = regex.get_ascii_regex(14, True)
    WRITER_IP_NUMBER = regex.get_ascii_regex(9)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, PUBLISHER_IP_NUMBER, PUBLISHER_NAME, SUBMITTER_AGREEMENT_NUMBER,
        SOCIETY_ASSIGNED_AGREEMENT_NUMBER, WRITER_IP_NUMBER)

    def __init__(self, record):
        super(WriterAgentRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._publisher_ip_number = self.get_value(19, 9)
        self._publisher_name = self.get_value(28, 45)
        self._submitter_agreement_number = self.get_integer_value(73, 14)
        self._society_assigned_agreement_number = self.get_integer_value(87, 14)
        self._writer_ip_number = self.get_value(101, 9)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()