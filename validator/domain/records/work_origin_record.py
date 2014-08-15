from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import INTENDED_PURPOSES
from validator.domain.values.avi_key import AviKey
from validator.domain.values.v_isan import VIsan


class WorkOriginRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Intended purpose', 'Production title', 'CD identifier', 'Cut number', 'Library',
                   'BLT', 'V_ISAN', 'Production ID', 'Episode title', 'Episode ID', 'Year of production', 'AVI key']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(3), regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(15, True), regex.get_numeric_regex(4, True), regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(1, True), VIsan.REGEX, regex.get_ascii_regex(12, True),
                   regex.get_ascii_regex(60, True), regex.get_ascii_regex(20, True), regex.get_numeric_regex(4, True),
                   AviKey.REGEX]

    def __init__(self, record, transaction):
        super(WorkOriginRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Cut number')
        self.attr_dict['V_ISAN'] = VIsan(self.attr_dict['V_ISAN'])
        self.format_integer_value('Year of production')
        self.attr_dict['AVI key'] = AviKey(self.attr_dict['AVI key'])

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'ORN':
            raise RecordRejectedError('ORN record type expected', self._record)

        if self.attr_dict['Intended purpose'] is not None and \
                self.attr_dict['Intended purpose'] not in INTENDED_PURPOSES:
            raise RecordRejectedError('Given intended purpose not in table', self._record, 'Intended purpose')

        if self.attr_dict['CD identifier'] != self.attr_dict['Cut number']:
            self.attr_dict['CD identifier'] = None
            self.attr_dict['Cut number'] = None
            self._rejected_fields['CD identifier'] = FieldRejectedError(
                'CD identifier and Cut number must be both blank or vice versa', self._record, 'CD identifier')
            self._rejected_fields['Cut number'] = FieldRejectedError(
                'CD identifier and Cut number must be both blank or vice versa', self._record, 'Cut number')

        if self.attr_dict['Intended purpose'] == 'LIB' and self.attr_dict['CD identifier'] is None:
                raise RecordRejectedError('Expected CD identifier for LIB intended purpose', self._record,
                                          'CD identifier')

        if self.attr_dict['Production title'] is None and self.attr_dict['Library'] is None:
            raise RecordRejectedError('Expected one of production title or library', self._record)

    def _validate_field(self, field_name):
        if field_name == 'Intended purpose':
            raise RecordRejectedError('Expected value', self._record, field_name)