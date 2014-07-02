__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import TIS_CODES
from validator.domain.record import Record


class PublisherTerritoryRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'SPT')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    IPA_NUMBER = regex.get_ascii_regex(9)
    CONSTANT = regex.get_optional_regex(6)
    PR_SHARE = regex.get_numeric_regex(5, True)
    MR_SHARE = regex.get_numeric_regex(5, True)
    SR_SHARE = regex.get_numeric_regex(5, True)
    INCLUSION_EXCLUSION = regex.get_defined_values_regex(1, False, 'E', 'I')
    TIS_NUMERIC_CODE = regex.get_numeric_regex(4)
    SHARES_CHANGE = regex.get_flag_regex(True)
    SEQUENCE_NUMBER = regex.get_numeric_regex(3)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, IPA_NUMBER, CONSTANT, PR_SHARE, MR_SHARE, SR_SHARE,
        INCLUSION_EXCLUSION, TIS_NUMERIC_CODE, SHARES_CHANGE, SEQUENCE_NUMBER)

    def __init__(self, record):
        super(PublisherTerritoryRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._registration_id = self.get_integer_value(3, 8)
        self._ipa_number = self.get_value(19, 9)
        self._pr_collection_share = self.get_float_value(34, 5, 3)
        self._mr_collection_share = self.get_float_value(39, 5, 3)
        self._sr_collection_share = self.get_float_value(44, 5, 3)
        self._excluded = self.get_value(49, 1) == 'E'
        self._tis_code = self.get_integer_value(50, 4)
        if self._tis_code not in TIS_CODES:
            raise ValueError('Given TIS code %d not in table' % self._tis_code)

        self._shares_change = self.get_value(54, 1) == 'Y'
        self._sequence_number = self.get_integer_value(55, 3)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()