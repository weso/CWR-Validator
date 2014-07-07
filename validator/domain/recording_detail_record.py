__author__ = 'Borja'
from barcode.ean import EAN13
from validator.cwr_utils import regex
from validator.domain.record import Record
from validator.cwr_utils.value_tables import MEDIA_TYPES
from validator.cwr_utils.value_tables import RECORDING_FORMAT
from validator.cwr_utils.value_tables import RECORDING_TECHNIQUE


class RecordingDetailRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'REC')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    FIRST_RELEASE_DATE = regex.get_date_regex(True)
    CONSTANT = regex.get_optional_regex(60)
    FIRST_RELEASE_DURATION = regex.get_time_regex(True)
    CONSTANT_TWO = regex.get_optional_regex(5)
    FIRST_ALBUM_TITLE = regex.get_ascii_regex(60, True)
    FIRST_ALBUM_LABEL = regex.get_ascii_regex(60, True)
    FIRST_RELEASE_CATALOG = regex.get_ascii_regex(18, True)
    EAN = regex.get_ascii_regex(13, True)
    ISRC = regex.get_ascii_regex(12, True)
    RECORDING_FORMAT = regex.get_alpha_regex(1, True)
    RECORDING_TECHNIQUE = regex.get_alpha_regex(1, True)
    MEDIA_TYPE = regex.get_ascii_regex(3, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, FIRST_RELEASE_DATE, CONSTANT, FIRST_RELEASE_DURATION,
        CONSTANT_TWO, FIRST_ALBUM_TITLE, FIRST_ALBUM_LABEL, FIRST_RELEASE_CATALOG, EAN, ISRC, RECORDING_FORMAT,
        RECORDING_TECHNIQUE, MEDIA_TYPE)

    def __init__(self, record):
        super(RecordingDetailRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._release_date = self.get_date_value(19, 8)
        self._release_duration = self.get_time_value(87, 6)
        self._album_title = self.get_value(98, 60)
        self._album_label = self.get_value(158, 60)
        self._release_catalog = self.get_value(218, 18)

        self._ean = self.get_value(236, 13)
        if self._ean is not None:
            self._ean = EAN13().to_ascii()

        self._isrc = self.get_value(249, 12)
        self._format = self.get_value(261, 1)
        if self._format is not None and self._format not in RECORDING_FORMAT:
            raise ValueError('Format %s not in recording formats' % self._format)

        self._technique = self.get_value(262, 1)
        if self._technique is not None and self._technique not in RECORDING_TECHNIQUE:
            raise ValueError('Technique %s not in recording techniques' % self._technique)

        self._media_type = self.get_value(263, 3)
        if self._media_type is not None and self._media_type not in MEDIA_TYPES:
            raise ValueError('Media type not in media types' % self._media_type)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()