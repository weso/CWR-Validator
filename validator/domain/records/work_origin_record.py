from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import INTENDED_PURPOSES
from validator.domain.records.record import Record
from validator.domain.values.avi_key import AviKey
from validator.domain.values.v_isan import VIsan


class WorkOriginRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Intended purpose', 'Production title', 'CD identifier', 'Cut number', 'Library',
                   'BLT', 'V_ISAN', 'Production ID', 'Episode title', 'Episode ID', 'Year of production', 'AVI key']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(3), regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(15, True), regex.get_numeric_regex(4, True), regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(1, True), VIsan.REGEX, regex.get_ascii_regex(12, True),
                   regex.get_ascii_regex(60, True), regex.get_ascii_regex(20, True), regex.get_numeric_regex(4, True),
                   AviKey.REGEX]

    def __init__(self, record):
        super(WorkOriginRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Cut number')
        self.attr_dict['V_ISAN'] = VIsan(self.attr_dict['V_ISAN'])
        self.format_integer_value('Year of production')
        self.attr_dict['AVI key'] = AviKey(self.attr_dict['AVI key'])

    def _build_record(self, record):
        if self.attr_dict['Record prefix'].record_type != 'ORN':
            raise FieldValidationError('ORN record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Intended purpose'] is not None:
            if self.attr_dict['Intended purpose'] not in INTENDED_PURPOSES:
                raise FieldValidationError('Given intended purpose: {} not in table'.format(
                    self.attr_dict['Intended purpose']))

        if self.attr_dict['CD identifier'] is not None and self.attr_dict['Cut number'] is None:
            raise FieldValidationError('CD identifier and Cut number must be both blank or vice versa')
        if self.attr_dict['CD identifier'] is None and self.attr_dict['Cut number'] is not None:
            raise FieldValidationError('CD identifier and Cut number must be both blank or vice versa')

        if self.attr_dict['Intended purpose'] == 'LIB':
            if self.attr_dict['CD identifier'] is None:
                raise FieldValidationError('Expected CD identifier for LIB intended purpose')

        if self.attr_dict['Production title'] is None and self.attr_dict['Library'] is None:
            raise FieldValidationError('Expected one of production title or library')