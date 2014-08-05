import abc
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.record import Record

__author__ = 'Borja'


class DetailHeader(Record):

    def __init__(self, record, transaction):
        if transaction is None:
            raise RecordRejectedError('Transaction must be valid', record)

        super(DetailHeader, self).__init__(record)
        self._transaction = transaction

    @property
    def transaction(self):
        return self._transaction

    @abc.abstractmethod
    def validate(self):
        pass

    @abc.abstractmethod
    def format(self):
        pass

    @abc.abstractmethod
    def _validate_field(self, field_name):
        pass
