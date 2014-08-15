from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.exceptions.transaction_rejected_error import TransactionRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import TIS_CODES


class PublisherTerritoryRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Interested party ID', 'Constant', 'PR collection share', 'MR collection share',
                   'SR collection share', 'Inclusion/Exclusion indicator', 'TIS numeric code', 'Shares change',
                   'Sequence ID']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(9), regex.get_optional_regex(6),
                   regex.get_numeric_regex(5, True), regex.get_numeric_regex(5, True), regex.get_numeric_regex(5, True),
                   regex.get_defined_values_regex(1, False, 'E', 'I'), regex.get_numeric_regex(4),
                   regex.get_boolean_regex(), regex.get_numeric_regex(3)]

    def __init__(self, record, transaction):
        super(PublisherTerritoryRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_float_value('PR collection share', 3)
        self.format_float_value('MR collection share', 3)
        self.format_float_value('SR collection share', 3)
        self.format_integer_value('TIS numeric code')
        self.format_integer_value('Sequence ID')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'SPT':
            raise RecordRejectedError('SPT record type expected', self._record, 'Record type')

        if self.attr_dict['TIS numeric code'] not in TIS_CODES:
            raise TransactionRejectedError(self._transaction, 'Given TIS numeric code not in table', self._record,
                                           'TIS numeric code')

        if 0 > self.attr_dict['PR collection share'] or self.attr_dict['PR collection share'] > 50:
            raise TransactionRejectedError('Expected share between 0 and 50', self._record, 'PR collection share')

        if 0 > self.attr_dict['MR collection share'] or self.attr_dict['MR collection share'] > 100:
            raise TransactionRejectedError('Expected share between 0 and 100', self._record, 'MR collection share')

        if 0 > self.attr_dict['SR collection share'] or self.attr_dict['SR collection share'] > 100:
            raise TransactionRejectedError('Expected share between 0 and 100', self._record, 'SR collection share')

        if self.attr_dict['Inclusion/Exclusion indicator'] == 'I' and \
            self.attr_dict['PR collection share'] == self.attr_dict['MR collection share'] == self.attr_dict[
                'SR collection share'] == 0:
            raise TransactionRejectedError(self._transaction, 'Expected one share to be greater than zero',
                                           self._record, 'Inclusion/Exclusion indicator')

    def _validate_field(self, field_name):
        if field_name == 'Inclusion/Exclusion indicator':
            raise TransactionRejectedError(self._transaction, 'Expected valid value', self._record, field_name)
        elif field_name == 'Shares change':
            self.attr_dict[field_name] = 'N'
            self._rejected_fields[field_name] = FieldRejectedError('Expected valid boolean value', self._record,
                                                                   field_name, 'N')
        elif field_name == 'Sequence number':
            raise RecordRejectedError('Expected value', self._record, field_name)