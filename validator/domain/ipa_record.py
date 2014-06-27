__author__ = 'Borja'
from validator.cwr_regex import regex
from validator.cwr_regex.value_tables import IPA_TYPES
from validator.cwr_regex.value_tables import SOCIETY_CODES
from validator.domain.record import Record


class InterestedPartyRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'IPA')
    AGREEMENT_ID = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)
    ROLE_CODE = regex.get_alpha_regex(2)
    CAE_IPI_NAME = regex.get_numeric_regex(11, True)
    IPI_BASE_NUMBER = regex.get_numeric_regex(13, True)
    IPA_NUMBER = regex.get_ascii_regex(9)
    IPA_LAST_NAME = regex.get_ascii_regex(45)
    IPA_FIRST_NAME = regex.get_ascii_regex(30, True)
    PR_AFFILIATION_SOCIETY = regex.get_numeric_regex(2, True) + regex.get_optional_regex(1)
    PR_SHARE = regex.get_numeric_regex(5)
    MR_AFFILIATION_SOCIETY = regex.get_numeric_regex(2, True) + regex.get_optional_regex(1)
    MR_SHARE = regex.get_numeric_regex(5)
    SR_AFFILIATION_SOCIETY = regex.get_numeric_regex(2, True) + regex.get_optional_regex(1)
    SR_SHARE = regex.get_numeric_regex(5)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}$".format(
        RECORD_TYPE, AGREEMENT_ID, RECORD_NUMBER, ROLE_CODE, CAE_IPI_NAME, IPI_BASE_NUMBER, IPA_NUMBER,
        IPA_LAST_NAME, IPA_FIRST_NAME, PR_AFFILIATION_SOCIETY, PR_SHARE, MR_AFFILIATION_SOCIETY, MR_SHARE,
        SR_AFFILIATION_SOCIETY, SR_SHARE)

    def __init__(self, record):
        super(InterestedPartyRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._agreement_id = int(record[3:3 + 8])
        self._role = record[19:19 + 2]
        if self._role not in IPA_TYPES:
            raise ValueError('Given role %s not in the specified types' % self._role)

        self._cae_number = int(record[21:21 + 11])
        if self._cae_number != 0:
            pass  # Check the number in some table?

        self._ipi_number = int(record[32:32 + 13])
        if self._ipi_number != 0:
            pass  # Check the number in some table?

        self._number = record[45:45 + 9]
        self._last_name = record[54:54 + 45]
        self._writer_first_name = record[99:99 + 30]
        if self._writer_first_name.strip():
            if self._role != 'AS':  # or related agreement  type not OS or OG
                raise ValueError('Not expected writer first name for role %s and agreement type %s'
                                 % (self._role, 'AGREEMENT_TYPE'))

        self._pr_share = float(record[132:132 + 3] + '.' + record[132 + 3:132 + 3 + 2])
        self._pr_society = int(record[129:129 + 3]) if record[129:129 + 3].strip() else None
        if self._pr_share > 0:
            if self._pr_society not in SOCIETY_CODES:  # Check pr_society within the table
                raise ValueError('Given PR Society  %s not in societies table' % self._pr_society)

        self._mr_share = float(record[140:140 + 3] + '.' + record[140 + 3:140 + 3 + 2])
        self._mr_society = int(record[137:137 + 3]) if record[137:137 + 3].strip() else None
        if self._mr_share > 0:
            if self._mr_society not in SOCIETY_CODES:  # Check pr_society within the table
                raise ValueError('Given MR Society  %s not in societies table' % self._mr_society)

        self._sr_share = float(record[148:148 + 3] + '.' + record[148 + 3:148 + 3 + 2])
        self._sr_society = int(record[145:145 + 3]) if record[145:145 + 3].strip() else None
        if self._sr_share > 0:
            if self._sr_society not in SOCIETY_CODES:  # Check pr_society within the table
                raise ValueError('Given SR Society  %s not in societies table' % self._sr_society)

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()