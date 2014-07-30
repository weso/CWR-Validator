__author__ = 'Borja'


class FileRejectedError(Exception):
    """ This exception causes the file being validated to be entire rejected"""

    def __init__(self, error, record=None, field=None):
        self.record = record
        self.field = field
        self.error = error

    def __str__(self):
        if self.record is None and self.field is None:
            error = self.error
        elif self.record is not None:
            error = '''The record: {} has caused the file to be rejected.
                       The cause is {}'''.format(self.record, self.error)
        else:
            error = '''The record: {} has caused the file to be rejected.
                       Causes are the field {} validation has thrown the error: {}'''.format(
                    self.record, self.field, self.error)

        return error