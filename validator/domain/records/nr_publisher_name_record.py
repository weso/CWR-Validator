from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.domain.records.record import Record


class NRPublisherNameRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Publisher sequence ID', 'Interested party ID', 'Publisher name', 'Language code']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_numeric_regex(2), regex.get_ascii_regex(9), regex.get_ascii_regex(480),
                   regex.get_alpha_regex(2, True)]

    def __init__(self, record):
        super(NRPublisherNameRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'NPN':
            raise FieldValidationError('NPN record type expected, obtained: {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            raise FieldValidationError('Given language code: {} not in table'.format(self.attr_dict['Language code']))