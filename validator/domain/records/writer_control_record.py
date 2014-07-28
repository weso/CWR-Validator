from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.cwr_utils.value_tables import WRITER_DESIGNATIONS
from validator.domain.records.record import Record


class WriterControlRecord(Record):
    S_AFF_REGEX = regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True)
    FIELD_NAMES = ['Record prefix', 'Interested party ID', 'Writer last name', 'Writer first name',
                   'Writer unknown indicator', 'Writer designation code', 'Tax ID number',
                   'Writer CAE/IPI name ID', 'PR affiliation society', 'PR ownership share',
                   'MR affiliation society', 'MR ownership share', 'SR affiliation society', 'SR ownership share',
                   'Reversionary indicator', 'First recording refusal indicator', 'Work for hire indicator',
                   'Filler', 'Writer IPI base number', 'Personal number', 'USA license indicator']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(9, True), regex.get_ascii_regex(45, True),
                   regex.get_ascii_regex(30, True), regex.get_flag_regex(True),
                   regex.get_alpha_regex(1, True) + regex.get_alpha_regex(1, True), regex.get_ascii_regex(9, True),
                   regex.get_numeric_regex(11, True), S_AFF_REGEX, regex.get_numeric_regex(5, True), S_AFF_REGEX,
                   regex.get_numeric_regex(5, True), S_AFF_REGEX, regex.get_numeric_regex(5, True),
                   regex.get_flag_regex(True), regex.get_boolean_regex(True), regex.get_boolean_regex(True),
                   regex.get_optional_regex(1), regex.get_ascii_regex(13, True), regex.get_numeric_regex(12, True),
                   regex.get_alpha_regex(1, True)]

    def __init__(self, record):
        super(WriterControlRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Tax ID number')
        self.format_integer_value('PR affiliation society')
        self.format_float_value('PR ownership share', 3)
        self.format_integer_value('MR affiliation society')
        self.format_float_value('MR ownership share', 3)
        self.format_integer_value('SR affiliation society')
        self.format_float_value('SR ownership share', 3)
        self.format_integer_value('Writer IPI base number')
        self.format_integer_value('Personal number')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type not in ['OWR', 'SWR']:
            raise FieldValidationError('OWR or SWR record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Record prefix'].record_type == 'SWR':
            if self.attr_dict['Interested party ID'] is None:
                raise FieldValidationError('Expected interested party ID for SWR record type')
            if self.attr_dict['Writer last name'] is None:
                raise FieldValidationError('Expected writer last name for SWR record type')
            if self.attr_dict['Writer unknown indicator'] is not None:
                raise FieldValidationError('Expected blank unknown indicator for SWR record type')
            if self.attr_dict['Writer designation code'] is None:
                raise FieldValidationError('Expected writer designation code for SWR record type')
            elif self.attr_dict['Writer designation code'] not in WRITER_DESIGNATIONS:
                raise FieldValidationError('Given writer designation code: {} not in table'.format(
                    self.attr_dict['Writer designation code']))
        else:
            if self.attr_dict['Writer unknown indicator'] == 'Y':
                if self.attr_dict['Writer last name'] is not None:
                    raise FieldValidationError('Expected blank writer last name for unknown indicator Y')

        if self.attr_dict['PR affiliation society'] is not None:
            if self.attr_dict['PR affiliation society'] not in SOCIETY_CODES:
                raise FieldValidationError('Given PR society: {} not in table'.format(
                    self.attr_dict['PR affiliation society']))

        if 0 > self.attr_dict['PR ownership share'] or self.attr_dict['PR ownership share'] > 100:
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