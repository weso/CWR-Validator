from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.domain.records.record import Record


class PerformingArtistRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Performing artist last name', 'Performing artist first name',
                   'Performing artist CAE/IPI name #', 'Performing artist IPI base number']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(45), regex.get_ascii_regex(30, True),
                   regex.get_ascii_regex(11, True), regex.get_ascii_regex(13, True)]

    def __init__(self, record):
        super(PerformingArtistRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Performing artist IPI base number')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'PER':
            raise FieldValidationError('PER record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))