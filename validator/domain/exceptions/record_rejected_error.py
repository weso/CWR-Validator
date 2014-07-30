__author__ = 'Borja'


class RecordRejectedError(Exception):
    """ This exception causes the record being validated to be entire rejected"""

    def __init__(self, error, record, field=None):
        self.record = record
        self.field = field
        self.error = error

    def __str__(self):
        if self.field is None:
            error = '''The record: {} has been rejected.
                  Causes are : {}'''.format(self.record, self.error)
        else:
            error = '''The record: {} has been rejected.
                    Causes are the field {} validation has thrown the error: {}'''.format(
                self.record, self.field, self.error)

        return error
