import abc
from validator.domain.records.record import Record

__author__ = 'Borja'


class TransactionHeader(Record):

    def __init__(self, record):
        super(TransactionHeader, self).__init__(record)
        self._records = {}

    @property
    def records(self):
        return self._records

    @abc.abstractmethod
    def validate(self):
        pass

    @abc.abstractmethod
    def format(self):
        pass

    @abc.abstractmethod
    def add_record(self, record):
        pass

    @abc.abstractmethod
    def validate_transaction(self):
        pass

    @abc.abstractmethod
    def _validate_field(self, field_name):
        pass