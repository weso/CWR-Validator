__author__ = 'Borja'


class FieldRejectedError(Exception):
    """ This exception causes the field being validated to be rejected and changed by a default value"""

    def __init__(self, error, record, field, default_value=None):
        self.record = record
        self.field = field
        self.value = default_value
        self.error = error

    def __str__(self):
        return '''The record: {} has a wrong field.
                  The field {} validation has thrown the error: {} and will be substituted with {}'''.format(
            self.record, self.field, self.error, self.value)
