# -*- encoding: utf-8 -*-

"""
Represents the CWR document being validated.
"""

__author__ = 'Borja Garrido Bear'
__license__ = 'MIT'
__version__ = '0.0.0'
__status__ = 'Development'


class Document(object):
    def __init__(self):
        self._header = None
        self._trailer = None

        self._groups = {}
        self._group_types = {}

        self._last_record = None
        self._rejected = False
        self._messages = []

        self._records_number = 0
        self._transactions_number = 0

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        self._header = header
        self._last_record = 'HDR'

    @property
    def trailer(self):
        return self._trailer

    @trailer.setter
    def trailer(self, trailer):
        self._trailer = trailer
        self._last_record = 'TRL'

    @property
    def rejected(self):
        return self._rejected

    @property
    def records_number(self):
        return self._records_number

    @property
    def transactions_number(self):
        return self._transactions_number

    def reject(self, record, message_text):
        from models.cwr_objects import CWRMessage

        msg = CWRMessage(CWRMessage.TYPES.FILE, 0, record.record_type, CWRMessage.TYPES.FILE, message_text)
        self._messages.append(msg)
        self._rejected = True

    def add_group(self, group):
        if self._last_record not in ['HDR', 'GRT']:
            self.reject(group, 'Group expected after HDR or GRT')

        if group.id.value != len(self._groups) + 1:
            group.group_reject('Groups expected in sequence')

        if group.transaction_type.value not in self._group_types.keys():
            self._groups[str(group.id.value)] = group
            self._group_types[group.transaction_type.value] = str(group.id.value)

        self._last_record = group.record_type.value

    def validate(self):
        self._header.file_level_validation(self)

        for group in self._groups.values():
            self._transactions_number += len(group.transactions)
            group.group_level_validation(group)
            group.file_level_validation(self)

        self._trailer.file_level_validation(self)

    def extract_records(self):
        records = [self._header]

        for group in self._groups.values():
            records.append(group)
            for transaction in group.transactions:
                records.append(transaction)
                records.extend(transaction.extract_records())
        records.append(self._trailer)

        self._records_number = len(records)

        return records