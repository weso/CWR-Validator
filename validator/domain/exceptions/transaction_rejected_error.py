__author__ = 'Borja'


class TransactionRejectedError(Exception):
    """ This exception causes the file being validated to be entire rejected"""

    def __init__(self, transaction, error, record=None, field=None):
        self.record = record
        self.field = field
        self.error = error
        self.transaction = transaction

    def __str__(self):
        if self.record is None and self.field is None:
            error = '''Transaction {} has been ejected, cause is {}'''.format(self.transaction, self.error)
        elif self.record is not None:
            error = '''The record: {} has caused the transaction {} to be rejected.
                       The cause is {}'''.format(self.record, self.transaction, self.error)
        else:
            error = '''The record: {} has caused the transaction {} to be rejected.
                       Causes are the field {} validation has thrown the error: {}'''.format(
                    self.record, self.transaction, self.field, self.error)

        return error