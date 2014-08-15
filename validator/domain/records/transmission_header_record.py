from validator.domain.exceptions.file_rejected_error import FileRejectedError

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import SENDER_VALUES
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.domain.records.record import Record


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
        self.format_integer_value('Sender ID')
        self.format_date_value('Creation date')
        self.format_time_value('Creation time')
        self.format_date_value('Transmission date')

    def validate(self):
        if not self._attr_dict['Sender type'] in SENDER_VALUES:
            raise FileRejectedError('Sender type not in required ones', self._record, 'Sender type')
        elif self._attr_dict['Sender ID'] is None:
            raise FileRejectedError('Sender ID must not be none', self._record, 'Sender ID')
        elif self._attr_dict['Sender type'] == 'SO' and self._attr_dict['Sender ID'] not in SOCIETY_CODES:
            raise FileRejectedError('Sender ID not in society codes', self._record, 'Sender ID')

        if self.attr_dict['Creation date'] is None:
            raise FileRejectedError('Creation date must be a valid date', self._record, 'Creation date')
        if self.attr_dict['Transmission date'] is None:
            raise FileRejectedError('Transmission date must be a valid date', self._record, 'Transmission date')

    def _validate_field(self, field_name):
        if field_name == 'Record type':
            raise FileRejectedError('Record type must be HDR', self._record, field_name)
        if field_name == 'EDI standard version number':
            raise FileRejectedError('EDI standard version number must be 01.10', self._record, field_name)