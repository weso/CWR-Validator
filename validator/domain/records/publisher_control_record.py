from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import AGREEMENT_TYPE_VALUES
from validator.cwr_utils.value_tables import PUBLISHER_TYPES
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.domain.records.record import Record


class PublisherControlRecord(Record):
    S_AFF_REGEX = regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True)

    FIELD_NAMES = ['Record prefix', 'Publisher sequence ID', 'Interested party ID', 'Publisher name',
                   'Publisher unknown indicator', 'Publisher type', 'Tax ID number', 'Publisher CAE/IPI name number',
                   'Submitter agreement number', 'PR affiliation society', 'PR ownership share',
                   'MR affiliation society', 'MR ownership share', 'SR affiliation society', 'SR ownership share',
                   'Reversionary indicator', 'First recording refusal indicator', 'Filler', 'Publisher IPI base number',
                   'International standard agreement code', 'Society assigned agreement number', 'Agreement type',
                   'USA license indicator']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_numeric_regex(2), regex.get_ascii_regex(9, True),
                   regex.get_ascii_regex(45, True), regex.get_flag_regex(True),
                   regex.get_alpha_regex(1, True) + regex.get_alpha_regex(1, True), regex.get_ascii_regex(9, True),
                   regex.get_numeric_regex(11, True), regex.get_ascii_regex(14, True), S_AFF_REGEX,
                   regex.get_numeric_regex(5, True), S_AFF_REGEX, regex.get_numeric_regex(5, True), S_AFF_REGEX,
                   regex.get_numeric_regex(5, True), regex.get_flag_regex(True), regex.get_flag_regex(True),
                   regex.get_optional_regex(1), regex.get_ascii_regex(13, True), regex.get_ascii_regex(14, True),
                   regex.get_ascii_regex(14, True), regex.get_alpha_regex(2, True), regex.get_alpha_regex(1, True)]

    def __init__(self, record):
        super(PublisherControlRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Publisher sequence ID')
        self.format_integer_value('Tax ID number')
        self.format_integer_value('Publisher CAE/IPI name number')
        self.format_integer_value('Submitter agreement number')
        self.format_integer_value('PR affiliation society')
        self.format_float_value('PR ownership share', 3)
        self.format_integer_value('MR affiliation society')
        self.format_float_value('MR ownership share', 3)
        self.format_integer_value('SR affiliation society')
        self.format_float_value('SR ownership share', 3)
        self.format_integer_value('Publisher IPI base number')
        self.format_integer_value('Society assigned agreement number')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type not in ['OPU', 'SPU']:
            raise FieldValidationError('OPU or SPU record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Record prefix'].record_type == 'SPU':
            if self.attr_dict['Interested party ID'] is None or self.attr_dict['Interested party ID'] == 0:
                raise FieldValidationError('Expected ipa number for SPU record')
            if self.attr_dict['Publisher name'] is None:
                raise FieldValidationError('Expected publisher name for SPU record')
            if self.attr_dict['Publisher type'] not in PUBLISHER_TYPES:
                raise FieldValidationError('Given publisher type: {} not in table'.format(
                    self.attr_dict['Publisher type']))
            if self.attr_dict['Publisher unknown indicator'] is not None:
                raise FieldValidationError('Expected blank unknown publisher indicator for SPU records')
        else:  # OPU record type
            if self.attr_dict['Publisher unknown indicator'] == 'Y':
                if self.attr_dict['Publisher name'] is not None:
                    raise FieldValidationError('Expected blank publisher name for publisher unknown indicator Y')
            if self.attr_dict['Publisher type'] not in PUBLISHER_TYPES:
                self.attr_dict['Publisher type'] = 'E'

        if self.attr_dict['PR affiliation society'] is not None:
            if self.attr_dict['PR affiliation society'] not in SOCIETY_CODES:
                raise FieldValidationError('Given PR society: {} not in table'.format(
                    self.attr_dict['PR affiliation society']))

        if 0 > self.attr_dict['PR ownership share'] or self.attr_dict['PR ownership share'] > 50:
            raise FieldValidationError('Expected PR share between 0 and 50, obtained {}'.format(
                self.attr_dict['PR ownership share']))
        elif self.attr_dict['PR ownership share'] > 0 and self.attr_dict['PR affiliation society'] is None:
            raise FieldValidationError('Expected PR society with share {}'.format(self.attr_dict['PR ownership share']))

        if self.attr_dict['MR affiliation society'] is not None:
            if self.attr_dict['MR affiliation society'] not in SOCIETY_CODES:
                raise FieldValidationError('Given MR society: {} not in table'.format(
                    self.attr_dict['MR affiliation society']))

        if 0 > self.attr_dict['MR ownership share'] or self.attr_dict['MR ownership share'] > 100:
            raise FieldValidationError('Expected MR share between 0 and 100, obtained {}'.format(
                self.attr_dict['MR ownership share']))
        elif self.attr_dict['MR ownership share'] > 0 and self.attr_dict['MR affiliation society'] is None:
            raise FieldValidationError('Expected MR society with share {}'.format(self.attr_dict['MR ownership share']))

        if self.attr_dict['SR affiliation society'] is not None:
            if self.attr_dict['SR affiliation society'] not in SOCIETY_CODES:
                raise FieldValidationError('Given SR society: {} not in table'.format(
                    self.attr_dict['SR affiliation society']))

        if 0 > self.attr_dict['SR ownership share'] or self.attr_dict['SR ownership share'] > 100:
            raise FieldValidationError('Expected SR share between 0 and 100, obtained {}'.format(
                self.attr_dict['SR ownership share']))
        elif self.attr_dict['SR ownership share'] > 0 and self.attr_dict['SR affiliation society'] is None:
            raise FieldValidationError('Expected SR society with share {}'.format(self.attr_dict['SR ownership share']))

        if self.attr_dict['Publisher type'] not in ['E', 'AQ']:
            if self.attr_dict['PR ownership share'] != self.attr_dict['MR ownership share'] != self.attr_dict[
                'SR ownership share'] != 0:
                raise FieldValidationError(
                    'All ownership shares must be equal to zero as this is not an original publisher')

        if self.attr_dict['PR affiliation society'] is None and self.attr_dict['MR affiliation society'] is None:
            raise FieldValidationError('Expected at least one PR or MR society')

        if self.attr_dict['Agreement type'] is not None:
            if self.attr_dict['Agreement type'] not in AGREEMENT_TYPE_VALUES:
                raise FieldValidationError('Given agreement type: {} not in table'.format(
                    self.attr_dict['Agreement type']))

        if self.attr_dict['USA license indicator'] not in [None, 'A', 'B', 'S']:
            raise FieldValidationError('Given USA license indicator: {} not in table'.format(
                self.attr_dict['USA license indicator']))