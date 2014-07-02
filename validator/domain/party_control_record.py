__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import AGREEMENT_TYPE_VALUES
from validator.cwr_utils.value_tables import PUBLISHER_TYPES
from validator.cwr_utils.value_tables import SOCIETY_CODES
from validator.domain.record import Record


class PartyControlRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'OPU', 'SPU')
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    PUBLISHER_NUMBER = regex.get_numeric_regex(2)
    INTERESTED_PARTY_NUMBER = regex.get_ascii_regex(9, True)
    PUBLISHER_NAME = regex.get_ascii_regex(45, True)
    UNKNOWN_PUBLISHER = regex.get_flag_regex(True)
    PUBLISHER_TYPE = regex.get_alpha_regex(1, True) + regex.get_alpha_regex(1, True)
    TAX_ID = regex.get_ascii_regex(9, True)
    PUBLISHER_CAE_NUMBER = regex.get_numeric_regex(11, True)
    SUBMITTER_AGREEMENT_NUMBER = regex.get_ascii_regex(14, True)
    PR_SOCIETY_NUMBER = regex.get_numeric_regex(2, True) + regex.get_optional_regex(1)
    PR_SHARE = regex.get_numeric_regex(5, True)
    MR_SOCIETY_NUMBER = regex.get_numeric_regex(2, True) + regex.get_optional_regex(1)
    MR_SHARE = regex.get_numeric_regex(5, True)
    SR_SOCIETY_NUMBER = regex.get_numeric_regex(2, True) + regex.get_optional_regex(1)
    SR_SHARE = regex.get_numeric_regex(5, True)
    REVERSIONARY_RIGHTS = regex.get_flag_regex(True)
    FIRST_RECORDING_REFUSAL = regex.get_flag_regex(True)
    FILLER = regex.get_optional_regex(1)
    PUBLISHER_IPI = regex.get_ascii_regex(13, True)
    INTERNATIONAL_STANDARD_AGREEMENT_CODE = regex.get_ascii_regex(14, True)
    SOCIETY_ASSIGNED_AGREEMENT_NUMBER = regex.get_ascii_regex(14, True)
    AGREEMENT_TYPE = regex.get_alpha_regex(2, True)
    USA_LICENSE = regex.get_flag_regex(True)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}{17}{18}{19}{20}{21}{22}{23}{24}$".format(
        RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER, PUBLISHER_NUMBER, INTERESTED_PARTY_NUMBER, PUBLISHER_NAME,
        UNKNOWN_PUBLISHER, PUBLISHER_TYPE, TAX_ID, PUBLISHER_CAE_NUMBER, SUBMITTER_AGREEMENT_NUMBER, PR_SOCIETY_NUMBER,
        PR_SHARE, MR_SOCIETY_NUMBER, MR_SHARE, SR_SOCIETY_NUMBER, SR_SHARE, REVERSIONARY_RIGHTS, FIRST_RECORDING_REFUSAL,
        FILLER, PUBLISHER_IPI, INTERNATIONAL_STANDARD_AGREEMENT_CODE, SOCIETY_ASSIGNED_AGREEMENT_NUMBER, AGREEMENT_TYPE,
        USA_LICENSE)

    def __init__(self, record):
        super(PartyControlRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._record_type = self.get_value(0, 3)
        self._registration_id = self.get_integer_value(3, 8)
        self._publisher_number = self.get_integer_value(19, 2)
        self._ipa_number = self.get_value(21, 9)
        if (self._ipa_number is None or self._ipa_number == 0) and self._record_type == 'SPU':
                raise ValueError('Expected ipa number for SPU record')

        self._publisher_name = self.get_value(30, 45)
        if not self._publisher_name is None and self._record_type == 'SPU':
                raise ValueError('Expected publisher name for SPU record')

        unknown_publisher = self.get_value(75, 1)
        if unknown_publisher is None:
            if self._publisher_name is None:
                raise ValueError('Unknown publisher indicator must be Y for OPU without publisher name')
        else:
            if self._record_type == 'SPU':
                raise ValueError('Unknown publisher indicator must be blank for SPU records')

        self._publisher_type = self.get_value(76, 2)
        if self._publisher_type not in PUBLISHER_TYPES:
            raise ValueError('Given publisher type %s not in table' % self._publisher_type)

        self._publisher_tax_id = self.get_integer_value(78, 9)
        self._publisher_cae_ipi = self.get_integer_value(87, 11)
        self._submitter_agreement_number = self.get_integer_value(98, 13)
        self._pr_share = self.get_float_value(115, 5, 3)
        self._pr_society = self.get_integer_value(112, 3)
        if self._pr_share is not None and self._pr_share > 0:
            if self._pr_share > 50:
                raise ValueError('PR share can\'t be greater than 50 within individual SPU records')
            if self._pr_society not in SOCIETY_CODES:
                raise ValueError('Given PR Society  %s not in societies table' % self._pr_society)

        self._mr_share = self.get_float_value(123, 5, 3)
        self._mr_society = self.get_integer_value(120, 3)
        if self._mr_share is not None and self._mr_share > 0:
            if self._mr_society not in SOCIETY_CODES:
                raise ValueError('Given MR Society  [%s] not in societies table' % self._mr_society)

        self._sr_share = self.get_float_value(131, 5, 3)
        self._sr_society = self.get_integer_value(128, 3)
        if self._sr_share is not None and self._sr_share > 0:
            if self._sr_society not in SOCIETY_CODES:
                raise ValueError('Given SR Society  %s not in societies table' % self._sr_society)

        self._reversionary = self.get_value(136, 1) == 'Y'
        self._recoding_refusal = self.get_value(137, 1) == 'Y'
        self._publisher_ipi = self.get_value(139, 13)
        self._international_agreement_code = self.get_value(152, 14)
        self._society_assigned_agreement_code = self.get_value(166, 14)
        self._agreement_type = self.get_value(180, 2)
        if self._agreement_type not in AGREEMENT_TYPE_VALUES:
            raise ValueError('Given agreement type %s not in table' % self._agreement_type)

        self._usa_license = self.get_value(182, 1) == 'Y'

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()