__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.domain.record import Record


class PerformingArtistRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'PER')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    PERFORMING_ARTIST_LAST_NAME = regex.get_ascii_regex(45)
    PERFORMING_ARTIST_FIRST_NAME = regex.get_ascii_regex(30, True)
    PERFORMING_ARTIST_IPI_CAE = regex.get_ascii_regex(11, True)
    PERFORMING_ARTIST_IPI_BASE = regex.get_ascii_regex(13, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, PERFORMING_ARTIST_LAST_NAME,
        PERFORMING_ARTIST_FIRST_NAME, PERFORMING_ARTIST_IPI_CAE, PERFORMING_ARTIST_IPI_BASE)

    def __init__(self, record):
        super(PerformingArtistRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._last_name = self.get_value(19, 45)
        self._first_name = self.get_value(64, 30)
        self._cae_ipi = self.get_integer_value(94, 11)
        self._ipi_base = self.get_integer_value(105, 13)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()