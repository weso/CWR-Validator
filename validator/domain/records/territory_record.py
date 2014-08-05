from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.exceptions.transaction_rejected_error import TransactionRejectedError
from validator.domain.records.detail_header_record import DetailHeader

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import TIS_CODES
from validator.domain.values.record_prefix import RecordPrefix


class TerritoryRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Inclusion/Exclusion indicator', 'TIS numeric code']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_defined_values_regex(1, False, 'E', 'I'), regex.get_numeric_regex(4)]

    def __init__(self, record, transaction):
        super(TerritoryRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('TIS numeric code')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'TER':
            raise RecordRejectedError('TER record type expected', self._record, 'Record type')

        if self.attr_dict['TIS numeric code'] not in TIS_CODES:
            raise TransactionRejectedError(self._transaction, 'Given TIS code not in table', self._record,
                                           'TIS numeric code')

    def _validate_field(self, field_name):
        if field_name == 'Inclusion/Exclusion indicator':
            raise TransactionRejectedError(self._transaction, 'Expected valid inclusion value',
                                           self._record, field_name)