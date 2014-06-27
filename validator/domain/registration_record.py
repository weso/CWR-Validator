__author__ = 'Borja'
from validator.cwr_regex import regex
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
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()
