from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES


class WorkExcerptTitle(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Entire work title', 'ISWC of entire work', 'Language code', 'Writer one last name',
                   'Writer one first name', 'Source', 'Writer one CAE/IPI name ID', 'Writer one IPI base number',
                   'Writer two last name', 'Writer two first name', 'Writer two CAE/IPI name ID',
                   'Writer two IPI base number', 'Submitter work ID']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(60), regex.get_ascii_regex(11, True),
                   regex.get_alpha_regex(2, True), regex.get_ascii_regex(45, True), regex.get_ascii_regex(30, True),
                   regex.get_ascii_regex(60, True), regex.get_numeric_regex(11, True),
                   regex.get_numeric_regex(13, True), regex.get_ascii_regex(45, True), regex.get_ascii_regex(30, True),
                   regex.get_numeric_regex(11, True), regex.get_numeric_regex(13, True),
                   regex.get_ascii_regex(14, True)]

    def __init__(self, record, transaction):
        super(WorkExcerptTitle, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Writer one IPI base number')
        self.format_integer_value('Writer two IPI base number')
        self.format_integer_value('Submitter work ID')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'EWT':
            raise RecordRejectedError('EWT record type expected', self._record)

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            self.attr_dict['Language code'] = None
            self._rejected_fields['Language code'] = FieldRejectedError('Given language code not in table',
                                                                        self._record, 'Language code')

    def _validate_field(self, field_name):
        if field_name == 'Entire work title':
            raise RecordRejectedError('Expected value', self._record, field_name)