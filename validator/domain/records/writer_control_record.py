__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.cwr_utils.value_tables import WRITER_DESIGNATIONS
from validator.domain.records.record import Record


class WriterControlRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'OWR', 'SWR')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    INTERESTED_PARTY_NUMBER = regex.get_ascii_regex(9, True)
    WRITER_LAST_NAME = regex.get_ascii_regex(45, True)
    WRITER_FIRST_NAME = regex.get_ascii_regex(30, True)
    UNKNOWN_WRITER = regex.get_flag_regex(True)
    WRITER_DESIGNATION_CODE = regex.get_alpha_regex(1, True) + regex.get_alpha_regex(1, True)
    TAX_ID = regex.get_ascii_regex(9, True)
    WRITER_CAE_NUMBER = regex.get_numeric_regex(11, True)
    PR_SOCIETY_NUMBER = regex.get_numeric_regex(2, True) + regex.get_optional_regex(1)
    PR_SHARE = regex.get_numeric_regex(5, True)
    MR_SOCIETY_NUMBER = regex.get_numeric_regex(2, True) + regex.get_optional_regex(1)
    MR_SHARE = regex.get_numeric_regex(5, True)
    SR_SOCIETY_NUMBER = regex.get_numeric_regex(2, True) + regex.get_optional_regex(1)
    SR_SHARE = regex.get_numeric_regex(5, True)
    REVERSIONARY_RIGHTS = regex.get_flag_regex(True)
    FIRST_RECORDING_REFUSAL = regex.get_flag_regex(True)
    WORK_FOR_HIRE = regex.get_flag_regex(True)
    FILLER = regex.get_optional_regex(1)
    WRITER_IPI = regex.get_ascii_regex(13, True)
    PERSONAL_NUMBER = regex.get_numeric_regex(12, True)
    USA_LICENSE = regex.get_flag_regex(True)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}{17}{18}{19}{20}{21}{22}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, INTERESTED_PARTY_NUMBER, WRITER_LAST_NAME, WRITER_FIRST_NAME,
        UNKNOWN_WRITER, WRITER_DESIGNATION_CODE, TAX_ID, WRITER_CAE_NUMBER, PR_SOCIETY_NUMBER, PR_SHARE,
        MR_SOCIETY_NUMBER, MR_SHARE, SR_SOCIETY_NUMBER, SR_SHARE, REVERSIONARY_RIGHTS, FIRST_RECORDING_REFUSAL,
        WORK_FOR_HIRE, FILLER, WRITER_IPI, PERSONAL_NUMBER, USA_LICENSE)

    def __init__(self, record):
        super(WriterControlRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._record_type = self.get_value(0, 3)
        self._registration_id = self.get_integer_value(3, 8)
        self._ipa_number = self.get_value(19, 9)
        if (self._ipa_number is None or self._ipa_number == 0) and self._record_type == 'SWR':
                raise ValueError('Expected ipa number for SWR record')

        self._writer_last_name = self.get_value(28, 45)
        if self._writer_last_name is None and self._record_type == 'SWR':
                raise ValueError('Expected publisher name for SWR record')

        self._writer_first_name = self.get_value(73, 30)
        unknown_writer = self.get_value(103, 1)
        if unknown_writer is None:
            if self._writer_last_name is None:
                raise ValueError('Unknown publisher indicator must be Y for OWR without publisher name')
        else:
            if self._record_type == 'SWR':
                raise ValueError('Unknown publisher indicator must be blank for SWR records')

        self._writer_type = self.get_value(104, 2)
        if self._writer_type not in WRITER_DESIGNATIONS:
            raise ValueError('Given publisher type %s not in table' % self._publisher_type)

        self._tax_id = self.get_integer_value(106, 9)
        self._writer_cae_ipi = self.get_integer_value(115, 11)
        self._pr_share = self.get_float_value(129, 5, 3)
        self._pr_society = self.get_integer_value(126, 3)
        if self._pr_society is not None and self._pr_society not in SOCIETY_CODES:
                raise ValueError('Given PR Society  %s not in societies table' % self._pr_society)

        self._mr_share = self.get_float_value(137, 5, 3)
        self._mr_society = self.get_integer_value(134, 3)
        if self._mr_society is not None and self._mr_society not in SOCIETY_CODES:
                raise ValueError('Given MR Society  [%s] not in societies table' % self._mr_society)

        self._sr_share = self.get_float_value(145, 5, 3)
        self._sr_society = self.get_integer_value(142, 3)
        if self._sr_society is not None and self._sr_society not in SOCIETY_CODES:
                raise ValueError('Given SR Society  %s not in societies table' % self._sr_society)

        self._reversionary = self.get_value(150, 1) == 'Y'
        self._recoding_refusal = self.get_value(151, 1) == 'Y'
        self._work_for_hire = self.get_value(152, 13)
        self._writer_ipi = self.get_value(154, 13)
        self._personal_number = self.get_integer_value(167, 12)
        self._usa_license = self.get_value(179, 1) == 'Y'

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()