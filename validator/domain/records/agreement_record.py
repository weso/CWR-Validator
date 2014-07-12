__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import AGREEMENT_TYPE_VALUES
from validator.domain.records.record import Record
from validator.domain.values.record_prefix import RecordPrefix


class AgreementRecord(Record):
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
        self.attr_dict['Submitter agreement number'] = self.format_integer_value(
            self.attr_dict['Submitter agreement number'])
        self.attr_dict['International standard agreement number'] = self.format_integer_value(
            self.attr_dict['International standard agreement number'])
        self.attr_dict['Agreement start date'] = self.format_date_value(self.attr_dict['Agreement start date'])
        self.attr_dict['Agreement end date'] = self.format_date_value(self.attr_dict['Agreement end date'])
        self.attr_dict['Retention end date'] = self.format_date_value(self.attr_dict['Retention end date'])
        self.attr_dict['Prior royalty start date'] = self.format_date_value(self.attr_dict['Prior royalty start date'])
        self.attr_dict['Post-term collection end date'] = self.format_date_value(
            self.attr_dict['Post-term collection end date'])
        self.attr_dict['Date of signature agreement'] = self.format_date_value(
            self.attr_dict['Date of signature agreement'])
        self.attr_dict['Number of works'] = self.format_integer_value(self.attr_dict['Number of works'])

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'AGR':
            raise ValueError('FIELD ERROR: AGR record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Agreement type'] not in AGREEMENT_TYPE_VALUES:
            raise ValueError('FIELD ERROR: Given agreement type: {} not in the required ones'.format(
                self.attr_dict['Agreement type']))

        if self.attr_dict['Agreement end date'] is not None and self.attr_dict['Retention end date'] is not None:
            if self.attr_dict['Retention end date'] < self.attr_dict['Agreement end date']:
                raise ValueError()

        if self.attr_dict['Prior royalty status'] == 'D':
            if self.attr_dict['Prior royalty start date'] is None:
                raise ValueError('Expecting royalty date')
            elif self.attr_dict['Prior royalty start date'] > self.attr_dict['Agreement start date']:
                raise ValueError()
        elif self.attr_dict['Prior royalty start date'] is not None:
            raise ValueError('Not expecting royalty date for royalty status %s' % self.attr_dict['Prior royalty start date'])

        if self.attr_dict['Post-term collection status'] == 'D':
            if self.attr_dict['Post-term collection end date'] is None:
                raise ValueError('Expecting Post-term collection end date')
            else:
                if self.attr_dict['Retention end date'] is not None and self.attr_dict['Post-term collection end date'] < self.attr_dict['Retention end date']:
                    raise ValueError()
                elif self.attr_dict['Agreement end date'] is not None and self.attr_dict['Post-term collection end date'] < self.attr_dict['Agreement end date']:
                    raise ValueError()
        elif self.attr_dict['Post-term collection end date'] is not None:
            raise ValueError('Not expecting royalty date for royalty status %s' % self.attr_dict['Post-term collection end date'])

        if self.attr_dict['Agreement type'] in ['OS', 'PS']:
            if self.attr_dict['Sales/Manufacture clause'] is None:
                raise ValueError('Sales clause not specified for an agreement type of %s' % self.attr_dict['Agreement type'])

        if self.attr_dict['Number of works'] <= 0:
            raise ValueError()