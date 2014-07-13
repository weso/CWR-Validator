__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import SENDER_VALUES
from validator.domain.records.record import Record

from validator.domain.exceptions.field_validation_error import FieldValidationError


class TransmissionHeaderRecord(Record):
    FIELD_NAMES = ['Record type', 'Sender type', 'Sender ID', 'Sender name', 'EDI Standard version number',
                   'Creation date', 'Creation time', 'Transmission date', 'Character set']

    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'HDR'), regex.get_alpha_regex(2),
                   regex.get_numeric_regex(9), regex.get_ascii_regex(45),
                   regex.get_defined_values_regex(5, False, '01\.10'), regex.get_date_regex(),
                   regex.get_time_regex(), regex.get_date_regex(), regex.get_alphanumeric_regex(15, True)]

    def __init__(self, record):
        super(TransmissionHeaderRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Sender ID'] = self.format_integer_value(self.attr_dict['Sender ID'])
        self.attr_dict['Creation date'] = self.format_date_value(self.attr_dict['Creation date'])
        self.attr_dict['Creation time'] = self.format_time_value(self.attr_dict['Creation time'])
        self.attr_dict['Transmission date'] = self.format_date_value(self.attr_dict['Transmission date'])

    def validate(self):
        if not self._attr_dict['Sender type'] in SENDER_VALUES:
            raise FieldValidationError('Given sender type: {} not in required ones'.format(
                self._attr_dict['Sender type']))