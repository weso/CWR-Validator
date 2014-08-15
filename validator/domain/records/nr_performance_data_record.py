from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES


class NRPerformanceDataRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Performing artist name', 'Performing artist first name',
                   'Performing artist IPI/CAE name ID', 'Performing artist IPI base number', 'Language code',
                   'Performance language', 'Performance dialect']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(160, True),regex.get_ascii_regex(160, True),
                   regex.get_ascii_regex(11, True), regex.get_ascii_regex(13, True), regex.get_alpha_regex(2, True),
                   regex.get_alpha_regex(2, True), regex.get_alpha_regex(3, True)]

    def __init__(self, record, transaction):
        super(NRPerformanceDataRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Performing artist IPI base number')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'NPR':
            raise RecordRejectedError('NPR record type expected', self._record)

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            self.attr_dict['Language code'] = None
            self._rejected_fields['Language code'] = FieldRejectedError('Given language code not in table',
                                                                        self._record, 'Language code')

        if self.attr_dict['Performance language'] is not None and \
                self.attr_dict['Performance language'] not in LANGUAGE_CODES:
            self.attr_dict['Performance language'] = None
            self._rejected_fields['Performance language'] = FieldRejectedError('Given language code not in table',
                                                                               self._record, 'Performance language')

        if self.attr_dict['Performing artist name'] is None and self.attr_dict['Performance language'] is None and \
                self.attr_dict['Performance dialect'] is None:
            raise RecordRejectedError('Expected at least one of performing artist, language or dialect fields',
                                      self._record)

    def _validate_field(self, field_name):
        pass