from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex


class WriterAgentRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Publisher IP ID', 'Publisher name', 'Submitter agreement number',
                   'Society assigned agreement number', 'Writer IP ID']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(9), regex.get_ascii_regex(45),
                   regex.get_ascii_regex(14, True), regex.get_ascii_regex(14, True), regex.get_ascii_regex(9)]

    def __init__(self, record, transaction):
        super(WriterAgentRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Submitter agreement number')
        self.format_integer_value('Society assigned agreement number')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'PWR':
            raise RecordRejectedError('PWR record type expected', self._record, 'Record type')

    def _validate_field(self, field_name):
        if field_name == 'Writer IP ID':
            raise RecordRejectedError('Expected value', self._record, field_name)