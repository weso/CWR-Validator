from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex


class WorkCompositeRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Title', 'ISWC of component', 'Submitter work ID', 'Duration',
                   'Writer one last name', 'Writer one first name', 'Writer one CAE/IPI name',
                   'Writer two last name', 'Writer two first name', 'Writer two CAE/IPI name',
                   'Writer one IPI base number', 'Writer two IPI base number']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(60), regex.get_ascii_regex(11, True),
                   regex.get_ascii_regex(14, True), regex.get_time_regex(True), regex.get_ascii_regex(45),
                   regex.get_ascii_regex(30, True), regex.get_numeric_regex(11, True), regex.get_ascii_regex(45, True),
                   regex.get_ascii_regex(30, True), regex.get_numeric_regex(11, True),
                   regex.get_numeric_regex(13, True), regex.get_numeric_regex(13, True)]

    def __init__(self, record, transaction):
        super(WorkCompositeRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_time_value('Duration')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'COM':
            raise RecordRejectedError('COM record type expected', self._record)

        if self.attr_dict['Writer two first name'] is not None and self.attr_dict['Writer two last name'] is None:
            self.attr_dict['Writer two first name'] = None
            self.attr_dict['Writer two last name'] = None
            raise FieldRejectedError('Expected writer two last name as first name is entered', self._record,
                                     'Writer two first name')
            raise FieldRejectedError('Expected writer two last name as first name is entered', self._record,
                                     'Writer two last name')

    def _validate_field(self, field_name):
        if field_name == 'Title':
            raise RecordRejectedError('Expected value', self._record, field_name)