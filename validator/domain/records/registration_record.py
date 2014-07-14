from validator.cwr_utils.value_tables import COMPOSITE_TYPE
from validator.cwr_utils.value_tables import DISTRIBUTION_CATEGORY_TABLE
from validator.cwr_utils.value_tables import EXCERPT_TYPE
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.cwr_utils.value_tables import LYRIC_ADAPTATION
from validator.cwr_utils.value_tables import MUSIC_ARRANGEMENT_TYPES
from validator.cwr_utils.value_tables import TEXT_MUSIC_TABLE
from validator.cwr_utils.value_tables import VERSION_TYPES
from validator.cwr_utils.value_tables import WORK_TYPES
from validator.cwr_utils import regex
from validator.domain.records.record import Record
from validator.domain.values.record_prefix import RecordPrefix
from validator.domain.exceptions.field_validation_error import FieldValidationError

__author__ = 'Borja'


class RegistrationRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Work title', 'Language code', 'Submitter work ID', 'ISWC', 'Copyright date',
                   'Copyright number', 'Musical work distribution category', 'Duration', 'Recorded indicator',
                   'Text music relationship', 'Composite type', 'Version type', 'Excerpt type', 'Music arrangement',
                   'Lyric adaptation', 'Contact name', 'Contact ID', 'CWR work type', 'Grand rights indicator',
                   'Composite component count', 'Date of publication of printed edition', 'Exceptional clause',
                   'Opus number', 'Catalogue number', 'Priority flag']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(60), regex.get_alpha_regex(2, True),
                   regex.get_ascii_regex(14), regex.get_ascii_regex(11, True), regex.get_date_regex(True),
                   regex.get_ascii_regex(12, True), regex.get_alpha_regex(3), regex.get_time_regex(True),
                   regex.get_flag_regex(), regex.get_alpha_regex(3, True), regex.get_alpha_regex(3, True),
                   regex.get_alpha_regex(3), regex.get_alpha_regex(3, True), regex.get_alpha_regex(3, True),
                   regex.get_alpha_regex(3, True), regex.get_ascii_regex(30, True), regex.get_ascii_regex(10, True),
                   regex.get_alpha_regex(2, True), regex.get_boolean_regex(True), regex.get_numeric_regex(3, True),
                   regex.get_date_regex(True), regex.get_flag_regex(True), regex.get_ascii_regex(25, True),
                   regex.get_ascii_regex(25, True), regex.get_flag_regex(True)]

    def __init__(self, record):
        super(RegistrationRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_date_value('Copyright date')
        self.format_time_value('Duration')
        self.format_integer_value('Composite component count')
        self.format_date_value('Date of publication of printed edition')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type not in ['NWR', 'REV']:
            raise FieldValidationError('NWR or REV record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            raise FieldValidationError('Given language code {} not in table'.format(self.attr_dict['Language code']))

        if self.attr_dict['Musical work distribution category'] not in DISTRIBUTION_CATEGORY_TABLE:
            raise FieldValidationError('Given distribution category {} not in table'.format(
                self.attr_dict['Musical work distribution category']))

        if self.attr_dict['Duration'] is None and self.attr_dict['Musical work distribution category'] ==  'SER':
                raise FieldValidationError('Expected duration for given work distribution {}'.format(
                    self.attr_dict['Musical work distribution category']))

        if self.attr_dict['Text music relationship'] is not None:
            if self.attr_dict['Text music relationship'] not in TEXT_MUSIC_TABLE:
                raise FieldValidationError('Given text music relationship: {} not in table'.format(
                    self.attr_dict['Text music relationship']))

        if self.attr_dict['Composite type'] is not None:
            if self.attr_dict['Composite type'] not in COMPOSITE_TYPE:
                raise FieldValidationError('Given composite type: {} not in table'.format(
                    self.attr_dict['Composite type']))
            if self.attr_dict['Composite component count'] is None or self.attr_dict['Composite component count'] <= 1:
                raise FieldValidationError('Expected component count')

        if self.attr_dict['Version type'] not in VERSION_TYPES:
            raise FieldValidationError('Given version type: {} not in table'.format(self.attr_dict['Version type']))

        if self.attr_dict['Excerpt type'] is not None and self.attr_dict['Excerpt type'] not in EXCERPT_TYPE:
                raise FieldValidationError('Given excerpt type: {} not in table'.format(self.attr_dict['Excerpt type']))

        if self.attr_dict['Version type'] == 'MOD':
            if self.attr_dict['Music arrangement'] is not None:
                if self.attr_dict['Music arrangement'] not in MUSIC_ARRANGEMENT_TYPES:
                    raise FieldValidationError('Given music arrangement type: {} not in table'.format(
                        self.attr_dict['Music arrangement']))
            else:
                raise FieldValidationError('Expected music arrangement for MOD version type')

            if self.attr_dict['Lyric adaptation'] is not None:
                if self.attr_dict['Lyric adaptation'] not in LYRIC_ADAPTATION:
                    raise FieldValidationError('Given lyric adaptation: {} not in table'.format(
                        self.attr_dict['Lyric adaptation']))
            else:
                raise FieldValidationError('Expected lyric adaptation for MOD version type')

        if self.attr_dict['CWR work type'] is not None and self.attr_dict['CWR work type'] not in WORK_TYPES:
                raise FieldValidationError('Given CWR work type: {} not in table'.format(
                    self.attr_dict['CWR work type']))