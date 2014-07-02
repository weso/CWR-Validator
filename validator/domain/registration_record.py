__author__ = 'Borja'
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
from validator.domain.record import Record


class RegistrationRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'NWR', 'REV')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    WORK_TITLE = regex.get_ascii_regex(60)
    LANGUAGE_CODE = regex.get_alpha_regex(2, True)
    SUBMITTER_WORK_NUMBER = regex.get_ascii_regex(14)
    ISWC = regex.get_ascii_regex(11, True)
    COPYRIGHT_DATE = regex.get_date_regex(True)
    COPYRIGHT_NUMBER = regex.get_ascii_regex(12, True)
    DISTRIBUTION_CATEGORY = regex.get_alpha_regex(3)
    DURATION = regex.get_time_regex(True)
    RECORDED_INDICATOR = regex.get_flag_regex()
    TEXT_MUSIC_RELATIONSHIP = regex.get_alpha_regex(3, True)
    COMPOSITE_TYPE = regex.get_alpha_regex(3, True)
    VERSION_TYPE = regex.get_defined_values_regex(3, False, 'MOD', 'ORI')
    EXCERPT_TYPE = regex.get_defined_values_regex(3, True, 'MOV', 'UEX')
    MUSIC_ARRANGEMENT = regex.get_alpha_regex(3, True)
    LYRIC_ADAPTATION = regex.get_alpha_regex(3, True)
    CONTACT_NAME = regex.get_ascii_regex(30, True)
    CONTACT_ID = regex.get_ascii_regex(10, True)
    WORK_TYPE = regex.get_alpha_regex(2, True)
    GRAND_RIGHTS = regex.get_flag_regex(True)
    COMPOSITE_COMPONENTS_COUNT = regex.get_numeric_regex(3, True)
    DATE_PUBLICATION = regex.get_date_regex(True)
    EXCEPTIONAL_CLAUSE = regex.get_flag_regex(True)
    OPUS_NUMBER = regex.get_ascii_regex(25, True)
    CATALOGUE_NUMBER = regex.get_ascii_regex(25, True)
    PRIORITY_FLAG = regex.get_flag_regex(True)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}{17}{18}{19}{20}{21}{22}{23}{24}{25}{26}{27}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, WORK_TITLE, LANGUAGE_CODE, SUBMITTER_WORK_NUMBER, ISWC,
        COPYRIGHT_DATE, COPYRIGHT_NUMBER, DISTRIBUTION_CATEGORY, DURATION, RECORDED_INDICATOR, TEXT_MUSIC_RELATIONSHIP,
        COMPOSITE_TYPE, VERSION_TYPE, EXCERPT_TYPE, MUSIC_ARRANGEMENT, LYRIC_ADAPTATION, CONTACT_NAME, CONTACT_ID,
        WORK_TYPE, GRAND_RIGHTS, COMPOSITE_COMPONENTS_COUNT, DATE_PUBLICATION, EXCEPTIONAL_CLAUSE, OPUS_NUMBER,
        CATALOGUE_NUMBER, PRIORITY_FLAG)

    def __init__(self, record):
        super(RegistrationRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._work_title = self.get_value(19, 60)
        self._language_code = self.get_value(79, 2)
        if self._language_code is not None and self._language_code not in LANGUAGE_CODES:
            raise ValueError('Given language code [%s] not in table' % self._language_code)

        self._work_submitter = self.get_value(81, 14)
        self._iswc = self.get_value(95, 11)
        self._copyright_date = self.get_date_value(106, 8)
        self._copyright_number = self.get_value(114, 12)
        self._distribution_category = self.get_value(126, 3)
        if self._distribution_category not in DISTRIBUTION_CATEGORY_TABLE:
            raise ValueError('Given distribution category %s is not valid' % self._distribution_category)

        self._duration = self.get_time_value(129, 6)
        if (self._duration is None or self._duration.microsecond == 0) and self._distribution_category in ['JAZ', 'SER']:
                raise ValueError('Duration must be specified within the given work distribution')

        self._recorded = self.get_value(135, 1) == 'Y'
        self._text_relationship = self.get_value(136, 3)
        if self._text_relationship is not None and self._text_relationship not in TEXT_MUSIC_TABLE:
                raise ValueError('Given Text-Music relationship %s not in table' % self._text_relationship)

        self._composite_type = self.get_value(139, 3)
        if self._composite_type is not None and self._composite_type not in COMPOSITE_TYPE:
                raise ValueError('Given composite type %s not in table' % self._composite_type)

        self._version_type = self.get_value(142, 3)
        if self._version_type not in VERSION_TYPES:
            raise ValueError('Given version type %s not in table' % self._version_type)

        self._excerpt_type = self.get_value(145, 3)
        if self._excerpt_type is not None and self._excerpt_type not in EXCERPT_TYPE:
                raise ValueError('Given excerpt type %s not in table' % self._excerpt_type)

        self._music_arrangement = self.get_value(148, 3)
        if self._version_type == 'MOD':
            if self._music_arrangement is not None:
                if self._music_arrangement not in MUSIC_ARRANGEMENT_TYPES:
                    raise ValueError('Given music arrangement type %s not in table' % self._music_arrangement)
            else:
                raise ValueError('Music arrangement required in MOD version types')

        self._lyric_adaptation = self.get_value(151, 3)
        if self._version_type == 'MOD':
            if self._lyric_adaptation is not None:
                if self._lyric_adaptation not in LYRIC_ADAPTATION:
                    raise ValueError('Given lyric adaptation %s not in table' % self._lyric_adaptation)
            else:
                raise ValueError('Lyric adaptation required in MOD version types')

        self._contact_name = self.get_value(154, 30)
        self._contact_id = self.get_value(184, 10)
        self._cwr_work_type = self.get_value(194, 2)
        if self._cwr_work_type is not None and self._cwr_work_type not in WORK_TYPES:
                raise ValueError('Given CWR Work type %s not in table' % self._cwr_work_type)

        self._grand_rights = self.get_value(196, 1) == 'Y'
        self._composite_count = self.get_integer_value(197, 3)
        self._printed_edition_pub_date = self.get_date_value(200, 8)
        self._exceptional_clause = self.get_value(208, 1) == 'Y'
        self._opus_number = self.get_value(209, 25)
        self._catalogue_number = self.get_value(234, 25)
        self._priority_flag = self.get_value(259, 1) == 'Y'

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()
