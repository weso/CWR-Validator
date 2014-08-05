from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.exceptions.transaction_rejected_error import TransactionRejectedError
from validator.domain.records.detail_header_record import DetailHeader

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import IPA_TYPES
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.domain.values.record_prefix import RecordPrefix


class InterestedPartyRecord(DetailHeader):
    S_AFF_REGEX = regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True)

    FIELD_NAMES = ['Record prefix', 'Agreement role code', 'Interested party CAE/IPI ID', 'IPI base number',
                   'Interested party ID', 'Interested party last name', 'Interested party writer first name',
                   'PR affiliation society', 'PR share', 'MR affiliation society', 'MR share', 'SR affiliation society',
                   'SR share']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_alpha_regex(2), regex.get_ascii_regex(11, True),
                   regex.get_numeric_regex(13, True), regex.get_ascii_regex(9), regex.get_ascii_regex(45),
                   regex.get_ascii_regex(30, True), S_AFF_REGEX, regex.get_numeric_regex(5), S_AFF_REGEX,
                   regex.get_numeric_regex(5), S_AFF_REGEX, regex.get_numeric_regex(5)]

    def __init__(self, record, transaction):
        super(InterestedPartyRecord, self).__init__(record, transaction)

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
            raise RecordRejectedError('IPA record type expected', self._record, 'Record type')

        if self.attr_dict['Agreement role code'] not in IPA_TYPES:
            raise TransactionRejectedError(self._transaction, 'Given agreement role code not in table',
                                           self._record, 'Agreement role code')

        if self.attr_dict['Interested party writer first name'] is not None:
            if self.attr_dict['Agreement role code'] != 'AS' or \
                    self._transaction.attr_dict['Agreement role code'] not in ['OS', 'OG']:
                raise FieldRejectedError('Not expected writer first name', self._record,
                                         'Interested party writer first name')

        if self.attr_dict['PR affiliation society'] is not None and \
                self.attr_dict['PR affiliation society'] not in SOCIETY_CODES:
            raise TransactionRejectedError(self._transaction, 'Given PR society not in table', self._record,
                                           'PR affiliation society')

        if 0 > self.attr_dict['PR share'] or self.attr_dict['PR share'] > 100:
            raise TransactionRejectedError(self._transaction, 'Expected share between 0 and 100', self._record,
                                           'PR share')
        elif self.attr_dict['PR share'] > 0 and self.attr_dict['PR affiliation society'] is None:
            raise TransactionRejectedError(self._transaction, 'Affiliation society expected', self._record,
                                           'PR share')

        if self.attr_dict['MR affiliation society'] is not None and \
                self.attr_dict['MR affiliation society'] not in SOCIETY_CODES:
            raise TransactionRejectedError(self._transaction, 'Given MR society not in table', self._record,
                                           'MR affiliation society')

        if 0 > self.attr_dict['MR share'] or self.attr_dict['MR share'] > 100:
            raise TransactionRejectedError(self._transaction, 'Expected share between 0 and 100', self._record,
                                           'MR share')
        elif self.attr_dict['MR share'] > 0 and self.attr_dict['MR affiliation society'] is None:
            raise TransactionRejectedError(self._transaction, 'Affiliation society expected', self._record,
                                           'MR share')

        if self.attr_dict['SR affiliation society'] is not None and \
                self.attr_dict['SR affiliation society'] not in SOCIETY_CODES:
            raise TransactionRejectedError(self._transaction, 'Given SR society not in table', self._record,
                                           'SR affiliation society')

        if 0 > self.attr_dict['SR share'] or self.attr_dict['SR share'] > 100:
            raise TransactionRejectedError(self._transaction, 'Expected share between 0 and 100', self._record,
                                           'SR share')
        elif self.attr_dict['SR share'] > 0 and self.attr_dict['SR affiliation society'] is None:
            raise TransactionRejectedError(self._transaction, 'Affiliation society expected', self._record,
                                           'SR share')

        if self.attr_dict['PR affiliation society'] is None and self.attr_dict['MR affiliation society'] is None:
            raise TransactionRejectedError(self._transaction, 'Expected at least one PR or MR society', self._record)

        if self.attr_dict['Agreement role code'] == 'AC' and \
                self.attr_dict['PR share'] == self.attr_dict['MR share'] == self.attr_dict['SR share'] == 0:
            raise TransactionRejectedError(self._transaction, 'At least one share expected to be greater than zero',
                                           self._record)

    def _validate_field(self, field_name):
        if field_name == 'Interested party last name':
            raise TransactionRejectedError(self._transaction, 'IPA last name must be entered', self._record,
                                           field_name)