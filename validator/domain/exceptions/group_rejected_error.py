__author__ = 'Borja'


class GroupRejectedError(Exception):
    """ This exception causes the group being validated to be entire rejected"""

    def __init__(self, group, error, record=None, field=None):
        self.group = group
        self.record = record
        self.field = field
        self.error = error

    def __str__(self):
        if self.record is None and self.field is None:
            error = '''The group {} has been rejected, cause: {}'''.format(self.group, self.error)
        elif self.record is not None and self.field is None:
            error = '''The record: {} has caused the group: {} to be rejected.
                  Causes are: {}'''.format(self.record, self.group, self.error)
        else:
            error = '''The record: {} has caused the group: {} to be rejected.
                  Causes are the field {} validation has thrown the error: {}'''.format(
                self.record, self.group, self.field, self.error)

        return error
