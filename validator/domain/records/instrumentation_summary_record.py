from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import INSTRUMENTATION_CODES


class InstrumentationSummaryRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Number of voices', 'Standard instrumentation type', 'Instrumentation description']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_numeric_regex(3, True), regex.get_ascii_regex(3, True),
                   regex.get_ascii_regex(50, True)]

    def __init__(self, record, transaction):
        super(InstrumentationSummaryRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Number of voices')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'INS':
            raise RecordRejectedError('INS record type expected', self._record)

        if self.attr_dict['Standard instrumentation type'] is not None and \
                self.attr_dict['Standard instrumentation type'] not in INSTRUMENTATION_CODES:
            raise RecordRejectedError('Given instrumentation type not in table', self._record,
                                      'Standard instrumentation type')

    def _validate_field(self, field_name):
        pass