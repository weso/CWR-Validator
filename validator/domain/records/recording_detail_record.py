from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from barcode.ean import EAN13

from validator.cwr_utils import regex
from validator.domain.records.record import Record
from validator.cwr_utils.value_tables import MEDIA_TYPES
from validator.cwr_utils.value_tables import RECORDING_FORMAT
from validator.cwr_utils.value_tables import RECORDING_TECHNIQUE


class RecordingDetailRecord(Record):
    FIELD_NAMES = ['Record prefix', 'First release date', 'Constant', 'First release duration', 'Constant',
                   'First album title', 'First album label', 'First release catalog ID', 'EAN', 'ISRC',
                   'Recording format', 'Recording technique', 'Media type']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_date_regex(True), regex.get_optional_regex(60),
                   regex.get_time_regex(True), regex.get_optional_regex(5), regex.get_ascii_regex(60, True),
                   regex.get_ascii_regex(60, True), regex.get_ascii_regex(18, True), regex.get_ascii_regex(13, True),
                   regex.get_ascii_regex(12, True), regex.get_alpha_regex(1, True), regex.get_alpha_regex(1, True),
                   regex.get_ascii_regex(3, True)]

    def __init__(self, record):
        super(RecordingDetailRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_date_value('First release date')
        self.format_time_value('First release duration')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'REC':
            raise FieldValidationError('SRC record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['EAN'] is not None:
            try:
                EAN13().to_ascii()
            except ValueError as msg:
                raise FieldValidationError(msg)

        if self.attr_dict['Recording format'] is not None:
            if self.attr_dict['Recording format'] not in RECORDING_FORMAT:
                raise FieldValidationError('Given recording format: {} not in table'.format(
                    self.attr_dict['Recording format']))

        if self.attr_dict['Recording technique'] is not None:
            if self.attr_dict['Recording technique'] not in RECORDING_TECHNIQUE:
                raise FieldValidationError('Given recording technique: {} not in table'.format(
                    self.attr_dict['Recording technique']))

        if self.attr_dict['Media type'] is not None and self.attr_dict['Media type'] not in MEDIA_TYPES:
            raise FieldValidationError('Given media type: {} not in table'.format(
                    self.attr_dict['Media type']))