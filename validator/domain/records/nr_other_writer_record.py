from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES


class NROtherWriterRecord(DetailHeader):
    FIELD_NAMES = ['Record type', 'Writer name', 'Writer first name', 'Language code', 'Writer position']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(160), regex.get_ascii_regex(160),
                   regex.get_alpha_regex(2, True), regex.get_alpha_regex(1, True)]

    def __init__(self, record, transaction):
        super(NROtherWriterRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Writer position')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'NOW':
            raise RecordRejectedError('NOW record type expected', self._record)

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            raise FieldRejectedError('Given language code not in table', self._record, 'Language code')

        if self.attr_dict['Writer position'] is not None and self.attr_dict['Writer position'] not in [1, 2]:
            self.attr_dict['Writer position'] = 1
            raise FieldRejectedError('Given writer position must be 1 or 2', self._record, 'Writer position', 1)

    def _validate_field(self, field_name):
        if field_name == 'Writer name':
            raise RecordRejectedError('Expected value', self._record, field_name)