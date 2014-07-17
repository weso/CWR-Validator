from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.cwr_utils.value_tables import TITLE_TYPES
from validator.domain.records.record import Record


class NRWorkTitleRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Title', 'Title type', 'Language code']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(640), regex.get_ascii_regex(2),
                   regex.get_alpha_regex(2, True)]

    def __init__(self, record):
        super(NRWorkTitleRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'NAT':
            raise FieldValidationError('NAT record type expected, obtained: {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Title type'] not in TITLE_TYPES:
            raise FieldValidationError('Given title type: {} not in table'.format(self.attr_dict['Title type']))

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            raise FieldValidationError('Given language code: {} not in table'.format(self.attr_dict['Language code']))

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()