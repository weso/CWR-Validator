from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.exceptions.transaction_rejected_error import TransactionRejectedError
from validator.domain.records.record import Record
from validator.domain.records.transaction_header_record import TransactionHeader

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import AGREEMENT_TYPE_VALUES
from validator.domain.values.record_prefix import RecordPrefix


class AgreementRecord(TransactionHeader):
    FIELD_NAMES = ['Record prefix', 'Submitter agreement number', 'International standard agreement number',
                   'Agreement type', 'Agreement start date', 'Agreement end date', 'Retention end date',
                   'Prior royalty status', 'Prior royalty start date', 'Post-term collection status',
                   'Post-term collection end date', 'Date of signature agreement', 'Number of works',
                   'Sales/Manufacture clause', 'Shares change', 'Advance given', 'Society-assigned agreement number']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_alphanumeric_regex(14), regex.get_alphanumeric_regex(14, True),
                   regex.get_alpha_regex(2), regex.get_date_regex(), regex.get_date_regex(True),
                   regex.get_date_regex(True), regex.get_defined_values_regex(1, False, 'A', 'D', 'N'),
                   regex.get_date_regex(True), regex.get_defined_values_regex(1, False, 'D', 'N', 'O'),
                   regex.get_date_regex(True), regex.get_date_regex(True), regex.get_numeric_regex(5),
                   regex.get_defined_values_regex(1, True, 'N', 'S'),
                   regex.get_boolean_regex(True), regex.get_boolean_regex(True), regex.get_alphanumeric_regex(14, True)]

    def __init__(self, record):
        super(AgreementRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Submitter agreement number')
        self.format_integer_value('International standard agreement number')
        self.format_date_value('Agreement start date')
        self.format_date_value('Agreement end date')
        self.format_date_value('Retention end date')
        self.format_date_value('Prior royalty start date')
        self.format_date_value('Post-term collection end date')
        self.format_date_value('Date of signature agreement')
        self.format_integer_value('Number of works')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'AGR':
            raise RecordRejectedError('AGR record type expected', self._record, 'Record prefix')

        if self.attr_dict['Agreement type'] not in AGREEMENT_TYPE_VALUES:
            raise TransactionRejectedError(self, 'Agreement type not in the required ones', self._record,
                                           'Agreement type')

        if self.attr_dict['Agreement end date'] is not None and self.attr_dict['Retention end date'] is not None:
            if self.attr_dict['Retention end date'] < self.attr_dict['Agreement end date']:
                raise TransactionRejectedError(self, 'Retention end date must be greater than agreement end date',
                                               self._record, 'Retention end date')

        if self.attr_dict['Prior royalty status'] == 'D':
            if self.attr_dict['Prior royalty start date'] is None:
                raise TransactionRejectedError(self, 'Expected royalty date for royalty status D', self._record,
                                               'Prior royalty start date')
            elif self.attr_dict['Prior royalty start date'] > self.attr_dict['Agreement start date']:
                raise TransactionRejectedError(self, 'Prior royalty start date must be lower than agreement start date',
                                               self._record, 'Prior royalty start date')
        elif self.attr_dict['Prior royalty start date'] is not None:
            raise TransactionRejectedError(self, 'Not expected royalty date for given royalty status', self._record,
                                           'Prior royalty start date')

        if self.attr_dict['Post-term collection status'] == 'D':
            if self.attr_dict['Post-term collection end date'] is None:
                raise TransactionRejectedError(self, 'Expected post-term collection end date for collection status D',
                                               self._record, 'Post-term collection end date')
            elif self.attr_dict['Retention end date'] is not None:
                if self.attr_dict['Post-term collection end date'] < self.attr_dict['Retention end date']:
                    raise TransactionRejectedError(self,
                                                   "Post-term collection end date must be greater than retention end date",
                                                   self._record, 'Post-term collection end date')
            elif self.attr_dict['Agreement end date'] is not None:
                if self.attr_dict['Post-term collection end date'] < self.attr_dict['Agreement end date']:
                    raise TransactionRejectedError(self,
                                                   "Post-term collection end date must be greater than agreement end date",
                                                   self._record, 'Post-term collection end date')
        elif self.attr_dict['Post-term collection end date'] is not None:
            raise TransactionRejectedError(self, 'Not expected post-term collection end date for given royalty status',
                                           self._record, 'Post-term collection end date')

        if self.attr_dict['Agreement type'] in ['OS', 'PS']:
            if self.attr_dict['Sales/Manufacture clause'] is None:
                raise TransactionRejectedError(self, 'Expected sales clause for given agreement type', self._record,
                                               'Sales/Manufacture clause')

        if self.attr_dict['Number of works'] <= 0:
            raise TransactionRejectedError(self, 'Number of works must be greater than zero', self._record,
                                           'Number of works')

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError('Expected a record object, not the string')

        if record.attr_dict['Record prefix'].record_type not in ['TER', 'IPA', 'NPA']:
            raise TransactionRejectedError(self, 'Trying to add a non compatible record type to agreement', record,
                                           'Record type')

        if record.attr_dict['Record prefix'].record_type not in self._records.keys():
            self._records[record.attr_dict['Record prefix'].record_type] = []

        self._records[record.attr_dict['Record prefix'].record_type].append(record)

    def _validate_field(self, field_name):
        if field_name in ['Agreement start date', 'Agreement end date', 'Retention end date',
                          'Prior royalty start date', 'Post-term collection end date']:
            raise TransactionRejectedError(self, 'Expected a valid date', self._record, field_name)
        if field_name in ['Prior royalty status', 'Post-term collection status']:
            raise TransactionRejectedError(self, 'Expected a valid status', self._record, field_name)
        if field_name == 'Date of signature agreement':
            self.attr_dict[field_name] = None
            raise FieldRejectedError('Expected a valid date', self._record, field_name)
        if field_name in ['Shared change', 'Advance given']:
            self.attr_dict[field_name] = 'N'
            raise FieldRejectedError('Expected a valid boolean value', self._record, field_name, 'N')

    def validate_transaction(self):
        if 'TER' not in self._records.keys():
            raise TransactionRejectedError(self, 'Expected at least one territory record for the agreement')

        if 'IPA' not in self._records.keys() or len(self._records['IPA']) < 2:
            raise TransactionRejectedError(self, 'Expected at least two ipa record for the agreement')

        pr_share = 0
        mr_share = 0
        sr_share = 0
        for ipa in self._records['IPA']:
            pr_share += ipa.attr_dict['PR share']
            mr_share += ipa.attr_dict['MR share']
            sr_share += ipa.attr_dict['SR share']

            if pr_share > 100:
                raise TransactionRejectedError(self, 'PR share exceeds a 100%')
            elif mr_share > 100:
                raise TransactionRejectedError(self, 'MR share exceeds a 100%')
            elif sr_share > 100:
                raise TransactionRejectedError(self, 'SR share exceeds a 100%')