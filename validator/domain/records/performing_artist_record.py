from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex


class PerformingArtistRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Performing artist last name', 'Performing artist first name',
                   'Performing artist CAE/IPI name #', 'Performing artist IPI base number']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(45), regex.get_ascii_regex(30, True),
                   regex.get_ascii_regex(11, True), regex.get_ascii_regex(13, True)]

    def __init__(self, record, transaction):
        super(PerformingArtistRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Performing artist IPI base number')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'PER':
            raise RecordRejectedError('PER record type expected', self._record)

    def _validate_field(self, field_name):
        if field_name == 'Artist last name':
            raise RecordRejectedError('Expected value', self._record, field_name)