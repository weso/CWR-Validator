__author__ = 'Borja'
from validator.cwr_regex import regex
from validator.cwr_regex.value_tables import AGREEMENT_TYPE_VALUES
from validator.cwr_regex.value_tables import PUBLISHER_TYPES
from validator.cwr_regex.value_tables import SOCIETY_CODES
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
        self._record_type = record[0:0 + 3]
        self._registration_id = int(record[3:3 + 8])
        self._publisher_number = int(record[19:19 + 2])
        self._ipa_number = record[21:21 + 9]
        if not self._ipa_number.strip():
            if self._record_type == 'SPU':
                raise ValueError('Expected ipa number for SPU record')
        else:
            self._ipa_number = int(self._ipa_number.strip())

        self._publisher_name = record[30:30 + 45]
        if not self._publisher_name.strip():
            if self._record_type == 'SPU':
                raise ValueError('Expected publisher name for SPU record')

        unknown_publisher = record[75:75 + 1]
        if not unknown_publisher.strip():
            if not self._publisher_name.strip():
                raise ValueError('Unknown publisher indicator must be Y for OPU without publisher name')
        else:
            if self._record_type == 'SPU':
                raise ValueError('Unknown publisher indicator must be blank for SPU records')

        self._publisher_type = record[76:76 + 2]
        if self._publisher_type.strip() not in PUBLISHER_TYPES:
            raise ValueError('Given publisher type %s not in table' % self._publisher_type)

        self._publisher_tax_id = record[78:78 + 9].strip()
        if self._publisher_tax_id:
            self._publisher_tax_id = int(self._publisher_tax_id)

        self._publisher_cae_ipi = record[87:87 + 11].strip()
        if self._publisher_cae_ipi:
            self._publisher_cae_ipi = int(self._publisher_cae_ipi)

        self._submitter_agreement_number = record[98:98 + 13].strip()
        if self._submitter_agreement_number:
            self._submitter_agreement_number = int(self._submitter_agreement_number)

        self._pr_share = float(record[115:115 + 3] + '.' + record[115 + 3:115 + 3 + 2])
        self._pr_society = int(record[112:112 + 3]) if record[129:129 + 3].strip() else None
        if self._pr_share > 0:
            if self._pr_share > 50:
                raise ValueError('PR share can\'t be greater than 50 within individual SPU records')
            if self._pr_society not in SOCIETY_CODES:  # Check pr_society within the table
                raise ValueError('Given PR Society  %s not in societies table' % self._pr_society)

        self._mr_share = float(record[123:123 + 3] + '.' + record[123 + 3:123 + 3 + 2])
        self._mr_society = int(record[120:120 + 3]) if record[120:120 + 3].strip() else None
        if self._mr_share > 0:
            if self._mr_society not in SOCIETY_CODES:  # Check pr_society within the table
                raise ValueError('Given MR Society  [%s] not in societies table' % self._mr_society)

        self._sr_share = float(record[131:131 + 3] + '.' + record[131 + 3:131 + 3 + 2])
        self._sr_society = int(record[128:128 + 3]) if record[128:128 + 3].strip() else None
        if self._sr_share > 0:
            if self._sr_society not in SOCIETY_CODES:  # Check pr_society within the table
                raise ValueError('Given SR Society  %s not in societies table' % self._sr_society)

        self._reversionary = True if record[136:136 + 1] == 'Y' else False
        self._recoding_refusal = True if record[137:137 + 1] == 'Y' else False
        self._publisher_ipi = record[139:139 + 13]
        self._international_agreement_code = record[152:152 + 14]
        self._society_assigned_agreement_code = record[166:166 + 14]
        self._agreement_type = record[180:180 + 2]
        if self._agreement_type not in AGREEMENT_TYPE_VALUES:
            raise ValueError('Given agreement type %s not in table' % self._agreement_type)

        self._usa_license = True if record[182:182 + 1] else False

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()