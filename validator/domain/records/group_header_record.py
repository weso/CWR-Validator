from validator.domain.exceptions.group_rejected_error import GroupRejectedError
from validator.domain.records.group_trailer_record import GroupTrailerRecord
from validator.domain.records.transaction_header_record import TransactionHeader

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import TRANSACTION_VALUES
from validator.domain.records.record import Record


class GroupHeaderRecord(Record):
    FIELD_NAMES = ['Record type', 'Transaction type', 'Group ID', 'Transaction type version number',
                   'Batch request', 'Submission/Distribution type']

    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'GRH'), regex.get_alpha_regex(3),
                   regex.get_numeric_regex(5), regex.get_defined_values_regex(5, False, '02\.10'),
                   regex.get_numeric_regex(10, True), regex.get_optional_regex(2)]

    def __init__(self, record):
        super(GroupHeaderRecord, self).__init__(record)
        self._transactions = {}
        self._trailer = None
        self._transactions_number = 0
        self._records_number = 0

    def format(self):
        self.format_integer_value('Group ID')
        self.format_integer_value('Batch request')

    def validate(self):
        if self.attr_dict['Transaction type'] not in TRANSACTION_VALUES:
            raise GroupRejectedError('Given transaction type not in required ones', self._record, 'Transaction type')

    def _validate_field(self, field_name):
        if field_name == 'Transaction type version number':
            raise GroupRejectedError('Version number must be 02.10', self._record, field_name)

    def add_transaction(self, transaction):
        if not isinstance(transaction, TransactionHeader):
            raise ValueError('Expected transaction to be a record object')

        self._transactions[transaction.attr_dict['Record prefix'].transaction_number] = transaction

    def add_trailer(self, trailer):
        if not isinstance(trailer, GroupTrailerRecord):
            raise ValueError('Expected trailer to be a record object')

        self._trailer = trailer

    def inc_transactions(self):
        self._transactions_number += 1

    def inc_records(self):
        self._records_number += 1

    @property
    def trailer(self):
        return self._trailer

    @property
    def transactions(self):
        return self._transactions

    @property
    def transactions_number(self):
        return self._transactions_number

    @property
    def records_number(self):
        return self._records_number