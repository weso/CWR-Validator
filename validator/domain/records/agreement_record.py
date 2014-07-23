from validator.domain.exceptions.document_validation_error import DocumentValidationError
from validator.domain.exceptions.field_validation_error import FieldValidationError
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
            raise FieldValidationError('AGR record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Agreement type'] not in AGREEMENT_TYPE_VALUES:
            raise FieldValidationError('Given agreement type: {} not in the required ones'.format(
                self.attr_dict['Agreement type']))

        if self.attr_dict['Agreement end date'] is not None and self.attr_dict['Retention end date'] is not None:
            if self.attr_dict['Retention end date'] < self.attr_dict['Agreement end date']:
                raise FieldValidationError('Retention end date must be greater than agreement end date')

        if self.attr_dict['Prior royalty status'] == 'D':
            if self.attr_dict['Prior royalty start date'] is None:
                raise FieldValidationError('Expected royalty date for royalty status D')
            elif self.attr_dict['Prior royalty start date'] > self.attr_dict['Agreement start date']:
                raise FieldValidationError('Prior royalty start date must be lower than agreement start date')
        elif self.attr_dict['Prior royalty start date'] is not None:
            raise FieldValidationError('Not expected royalty date for royalty status {}'.format(
                self.attr_dict["Prior royalty start date"]))

        if self.attr_dict['Post-term collection status'] == 'D':
            if self.attr_dict['Post-term collection end date'] is None:
                raise FieldValidationError('Expected post-term collection end date for collection status D')
            else:
                if self.attr_dict['Retention end date'] is not None:
                    if self.attr_dict['Post-term collection end date'] < self.attr_dict['Retention end date']:
                        raise FieldValidationError(
                            "Post-term collection end date must be greater than retention end date")
                elif self.attr_dict['Agreement end date'] is not None:
                    if self.attr_dict['Post-term collection end date'] < self.attr_dict['Agreement end date']:
                        raise FieldValidationError(
                            "Post-term collection end date must be greater than agreement end date")
        elif self.attr_dict['Post-term collection end date'] is not None:
            raise FieldValidationError('Not expected post-term collection end date for royalty status {}'.format(
                self.attr_dict['Post-term collection end date']))

        if self.attr_dict['Agreement type'] in ['OS', 'PS']:
            if self.attr_dict['Sales/Manufacture clause'] is None:
                raise FieldValidationError('Expected sales clause for an agreement type of {}'.format(
                    self.attr_dict['Agreement type']))

        if self.attr_dict['Number of works'] <= 0:
            raise FieldValidationError('Number of works must be greater than zero')

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError('Expected a record object, not the string')

        if record.attr_dict['Record prefix'].record_type not in ['TER', 'IPA', 'NPA']:
            raise DocumentValidationError('Trying to add a non compatible record type: {} to agreement'.format(
                record.attr_dict['Record prefix'].record_type))

        if record.attr_dict['Record prefix'].record_type not in self._records.keys():
            self._records[record.attr_dict['Record prefix'].record_type] = []

        self._records[record.attr_dict['Record prefix'].record_type].append(record)