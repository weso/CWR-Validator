__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import AGREEMENT_TYPE_VALUES
from validator.domain.record import Record


class AgreementRecord(Record):
    RECORD_TYPE = regex.get_defined_values_regex(3, False, 'AGR')
    AGREEMENT_NUMBER = regex.get_numeric_regex(16)
    SUBMITTER_NUMBER = regex.get_alphanumeric_regex(14)
    INTERNATIONAL_CODE = regex.get_alphanumeric_regex(14, True)
    AGREEMENT_TYPE = regex.get_alpha_regex(2)
    START_DATE = regex.get_date_regex()
    END_DATE = regex.get_date_regex(True)
    RETENTION_END_DATE = regex.get_date_regex(True)
    PRIOR_ROYALTY_STATUS = regex.get_defined_values_regex(1, False, 'A', 'D', 'N')
    PRIOR_ROYALTY_START_DATE = regex.get_date_regex(True)
    POST_TERM_COLLECTION_STATUS = regex.get_defined_values_regex(1, False, 'D', 'N', 'O')
    POST_TERM_COLLECTION_END_DATE = regex.get_date_regex(True)
    SIGNATURE_DATE = regex.get_date_regex(True)
    WORKS_NUMBER = regex.get_numeric_regex(5)
    SALES_CLAUSE = regex.get_defined_values_regex(1, True, 'N', 'S')
    SHARES_CHANGE = regex.get_flag_regex(True)
    ADVANCE_GIVEN = regex.get_flag_regex(True)
    SOCIETY_ASSIGNED_NUMBER = regex.get_alphanumeric_regex(14, True)

    REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}{17}$".format(
        RECORD_TYPE, AGREEMENT_NUMBER, SUBMITTER_NUMBER, INTERNATIONAL_CODE, AGREEMENT_TYPE, START_DATE, END_DATE,
        RETENTION_END_DATE, PRIOR_ROYALTY_STATUS, PRIOR_ROYALTY_START_DATE, POST_TERM_COLLECTION_STATUS,
        POST_TERM_COLLECTION_END_DATE, SIGNATURE_DATE, WORKS_NUMBER, SALES_CLAUSE, SHARES_CHANGE, ADVANCE_GIVEN,
        SOCIETY_ASSIGNED_NUMBER)

    def __init__(self, record):
        super(AgreementRecord, self).__init__(record, self.REGEX)

    def _build_record(self, record):
        self._number = self.get_integer_value(8, 3)
        self._submitter = self.get_value(19, 14)
        self._international_code = self.get_value(33, 14)
        self._type = self.get_value(47, 2)
        if self._type not in AGREEMENT_TYPE_VALUES:
            raise ValueError('Given agreement type: [%s] not in the required ones' % self._type)

        self._start_date = self.get_date_value(49, 8)
        self._end_date = self.get_date_value(57, 8)
        self._retention_end_date = self.get_date_value(65, 8)
        self._prior_royalty_status = self.get_value(73, 1)
        self._prior_royalty_date = self.get_date_value(74, 8)
        if self._prior_royalty_status == 'D':
            if self._prior_royalty_date is None:
                raise ValueError('Expecting royalty date')
        elif self._prior_royalty_date is not None:
            raise ValueError('Not expecting royalty date for royalty status %s' % self._prior_royalty_status)

        self._post_term_collection_stat = self.get_value(82, 1)
        self._post_term_collection_date = self.get_date_value(83, 8)
        if self._post_term_collection_stat == 'D':
            if self._post_term_collection_date is None:
                raise ValueError('Expecting post term collection date')
        elif self._post_term_collection_date is not None:
            raise ValueError('Not expecting post-term collection date for status %s' % self._post_term_collection_stat)

        self._signature_date = self.get_date_value(91, 8)
        self._works_number = self.get_integer_value(99, 5)
        self._sales_clause = self.get_value(104, 1)
        # Sales clause is only mandatory for OS and PS agreements
        if self._sales_clause is None:
            if self._type == 'OS' or self._type == 'PS':
                raise ValueError('Sales clause not specified for an agreement type of %s' % self._type)

        self._shares_change = self.get_value(105, 1) == 'T'
        self._advance_given = self.get_value(106, 1) == 'T'
        self._society_assigned_number = self.get_value(107, 14)

    def validate(self):
        pass

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()