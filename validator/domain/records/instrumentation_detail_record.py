from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import INSTRUMENT_CODES


class InstrumentationDetailRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Instrument code', 'Number of players']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_alpha_regex(3), regex.get_numeric_regex(3, True)]

    def __init__(self, record, transaction):
        super(InstrumentationDetailRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Number of players')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'IND':
            raise RecordRejectedError('IND record type expected', self._record)

        if self.attr_dict['Instrument code'] not in INSTRUMENT_CODES:
            raise RecordRejectedError('Given instrument code not in table', self._record, 'Instrument code')

    def _validate_field(self, field_name):
        if field_name == 'Instrument code':
            raise RecordRejectedError('Given instrument code not in table', self._record, 'Instrument code')
        elif field_name == 'Number of players':
            raise RecordRejectedError('Expected value', self._record, field_name)