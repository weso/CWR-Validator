from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import RIGHT_TYPES
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.cwr_utils.value_tables import SUBJECT_CODES


class WorkAdditionalInfoRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Society ID', 'Work ID', 'Type of right', 'Subject code', 'Note']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_numeric_regex(3), regex.get_ascii_regex(14, True),
                   regex.get_alpha_regex(3), regex.get_alpha_regex(2, True), regex.get_ascii_regex(160, True)]

    def __init__(self, record, transaction):
        super(WorkAdditionalInfoRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Society ID')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'ARI':
            raise RecordRejectedError('ARI record type expected', self._record)

        if self.attr_dict['Society ID'] not in SOCIETY_CODES:
            raise RecordRejectedError('Given society ID not in table', self._record, 'Society ID')

        if self.attr_dict['Right type'] not in RIGHT_TYPES:
            raise RecordRejectedError('Given right type not in table', self._record, 'Right type')

        if self.attr_dict['Note'] is not None and self.attr_dict['Subject code'] not in SUBJECT_CODES:
            raise RecordRejectedError('Given subject code not in table', self._record, 'Subject code')

    def _validate_field(self, field_name):
        pass