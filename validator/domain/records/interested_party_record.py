from validator.domain.exceptions.field_validation_error import FieldValidationError

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import IPA_TYPES
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.domain.records.record import Record
from validator.domain.values.record_prefix import RecordPrefix


class InterestedPartyRecord(Record):
    S_AFF_REGEX = regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True)

    FIELD_NAMES = ['Record prefix', 'Agreement role code', 'Interested party CAE/IPI ID', 'IPI base number',
                   'Interested party ID', 'Interested party last name', 'Interested party writer first name',
                   'PR affiliation society', 'PR share', 'MR affiliation society', 'MR share', 'SR affiliation society',
                   'SR share']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_alpha_regex(2), regex.get_ascii_regex(11, True),
                   regex.get_numeric_regex(13, True), regex.get_ascii_regex(9), regex.get_ascii_regex(45),
                   regex.get_ascii_regex(30, True), S_AFF_REGEX, regex.get_numeric_regex(5), S_AFF_REGEX,
                   regex.get_numeric_regex(5), S_AFF_REGEX, regex.get_numeric_regex(5)]

    def __init__(self, record):
        super(InterestedPartyRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Interested party CAE/IPI ID')
        self.format_integer_value('IPI base number')
        self.format_integer_value('PR affiliation society')
        self.format_float_value('PR share', 3)
        self.format_integer_value('MR affiliation society')
        self.format_float_value('MR share', 3)
        self.format_integer_value('SR affiliation society')
        self.format_float_value('SR share', 3)

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'IPA':
            raise FieldValidationError('IPA record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Agreement role code'] not in IPA_TYPES:
            raise FieldValidationError('Given agreement role code {} not in table'.format(
                self.attr_dict['Agreement role code']))

        if self.attr_dict['Interested party writer first name'] is not None:
            if self.attr_dict['Agreement role code'] != 'AS':  # or related agreement  type not OS or OG
                raise FieldValidationError('Not expected writer first name for role {} and agreement type {}'.format(
                    self.attr_dict['Agreement role code'], 'AGREEMENT_TYPE'))

        if self.attr_dict['PR affiliation society'] is not None:
            if self.attr_dict['PR affiliation society'] not in SOCIETY_CODES:
                raise FieldValidationError('Given PR society: {} not in table'.format(
                    self.attr_dict['PR affiliation society']))

        if 0 > self.attr_dict['PR share'] or self.attr_dict['PR share'] > 100:
            raise FieldValidationError('Expected PR share between 0 and 100, obtained {}'.format(
                self.attr_dict['PR share']))
        elif self.attr_dict['PR share'] > 0 and self.attr_dict['PR affiliation society'] is None:
            raise FieldValidationError('Expected PR society with share {}'.format(self.attr_dict['PR share']))

        if self.attr_dict['MR affiliation society'] is not None:
            if self.attr_dict['MR affiliation society'] not in SOCIETY_CODES:
                raise FieldValidationError('Given MR society: {} not in table'.format(
                    self.attr_dict['MR affiliation society']))

        if 0 > self.attr_dict['MR share'] or self.attr_dict['MR share'] > 100:
            raise FieldValidationError('Expected MR share between 0 and 100, obtained {}'.format(
                self.attr_dict['MR share']))
        elif self.attr_dict['MR share'] > 0 and self.attr_dict['MR affiliation society'] is None:
            raise FieldValidationError('Expected MR society with share {}'.format(self.attr_dict['MR share']))

        if self.attr_dict['SR affiliation society'] is not None:
            if self.attr_dict['SR affiliation society'] not in SOCIETY_CODES:
                raise FieldValidationError('Given SR society: {} not in table'.format(
                    self.attr_dict['SR affiliation society']))

        if 0 > self.attr_dict['SR share'] or self.attr_dict['SR share'] > 100:
            raise FieldValidationError('Expected SR share between 0 and 100, obtained {}'.format(
                self.attr_dict['SR share']))
        elif self.attr_dict['SR share'] > 0 and  self.attr_dict['SR affiliation society'] is None:
            raise FieldValidationError('Expected SR society with share {}'.format(self.attr_dict['SR share']))

        if self.attr_dict['PR affiliation society'] is None and self.attr_dict['MR affiliation society'] is None:
            raise FieldValidationError('Expected at least one PR or MR society')
