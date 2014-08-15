from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.exceptions.transaction_rejected_error import TransactionRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.cwr_utils.value_tables import WRITER_DESIGNATIONS


class WriterControlRecord(DetailHeader):
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

    def __init__(self, record, transaction):
        super(WriterControlRecord, self).__init__(record, transaction)

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
            raise RecordRejectedError('OWR or SWR record type expected', self._record, 'Record type')

        if self.attr_dict['Record prefix'].record_type == 'SWR':
            if self.attr_dict['Interested party ID'] is None:
                raise TransactionRejectedError(self._transaction, 'Expected interested party ID for SWR record type',
                                               self._record, 'Interested party ID')
            if self.attr_dict['Writer last name'] is None:
                raise TransactionRejectedError(self._transaction, 'Expected writer last name for SWR record type',
                                               self._record, 'Writer last name')
            if self.attr_dict['Writer unknown indicator'] is not None:
                raise TransactionRejectedError(self._transaction, 'Expected blank unknown indicator for SWR record',
                                               self._record, 'Writer unknown indicator')
            if self.attr_dict['Writer designation code'] not in WRITER_DESIGNATIONS:
                raise TransactionRejectedError(self._transaction, 'Given writer designation code not in table',
                                               self._record, 'Writer designation code')
        else:
            if self.attr_dict['Writer unknown indicator'] == 'Y' and \
                    self.attr_dict['Writer last name'] is not None:
                raise TransactionRejectedError(self._transaction, '''Expected blank writer last name for unknown
                indicator Y''', self._record, 'Writer last name')

        if self.attr_dict['PR affiliation society'] is not None and \
                self.attr_dict['PR affiliation society'] not in SOCIETY_CODES:
            raise TransactionRejectedError(self._transaction, 'Given society not in table', self._record,
                                           'PR affiliation society')

        if 0 > self.attr_dict['PR ownership share'] or self.attr_dict['PR ownership share'] > 100:
            raise TransactionRejectedError(self._transaction, 'Expected share between 0 and 50', self._record,
                                           'PR ownership share')
        elif self.attr_dict['PR ownership share'] > 0 and self.attr_dict['PR affiliation society'] is None:
            raise TransactionRejectedError(self._transaction, 'Expected society', self._record, 'PR affiliation society')

        if self.attr_dict['MR affiliation society'] is not None and \
                self.attr_dict['MR affiliation society'] not in SOCIETY_CODES:
            raise TransactionRejectedError(self._transaction, 'Given society not in table', self._record,
                                           'MR affiliation society')

        if 0 > self.attr_dict['MR ownership share'] or self.attr_dict['MR ownership share'] > 100:
            raise TransactionRejectedError(self._transaction, 'Expected share between 0 and 100', self._record,
                                           'MR ownership share')
        elif self.attr_dict['MR ownership share'] > 0 and self.attr_dict['MR affiliation society'] is None:
            raise TransactionRejectedError(self._transaction, 'Expected society', self._record, 'PR affiliation society')

        if self.attr_dict['SR affiliation society'] is not None and \
                self.attr_dict['SR affiliation society'] not in SOCIETY_CODES:
            raise TransactionRejectedError(self._transaction, 'Given society not in table', self._record,
                                           'SR affiliation society')

        if 0 > self.attr_dict['SR ownership share'] or self.attr_dict['SR ownership share'] > 100:
            raise TransactionRejectedError(self._transaction, 'Expected share between 0 and 100', self._record,
                                           'SR ownership share')
        elif self.attr_dict['SR ownership share'] > 0 and self.attr_dict['SR affiliation society'] is None:
            raise TransactionRejectedError(self._transaction, 'Expected society', self._record, 'PR affiliation society')

    def _validate_field(self, field_name):
        if field_name in ['Reversionary indicator', 'First recording refusal indicator', 'Work for hire indicator']:
            self._rejected_fields[field_name] = FieldRejectedError('Expected valid flag value', self._record,
                                                                   field_name)