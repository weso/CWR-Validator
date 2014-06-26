__author__ = 'Borja'
import datetime
import re


class AgreementRecord(object):
    AGREEMENT_TYPE_VALUES = {'OG', 'OS', 'PG', 'PS'}

    RECORD_TYPE = 'AGR'
    AGREEMENT_NUMBER = '\d{8}\d{8}'  # Not really clear in the document
    SUBMITTER_NUMBER = '[ -~]{14}'
    INTERNATIONAL_CODE = '[ -~]{14}'
    AGREEMENT_TYPE = '[A-Z]{2}'
    START_DATE = '\d{8}'
    END_DATE = '[ \d]{8}'  # Optional values are filled with whitespaces
    RETENTION_END_DATE = '[ \d]{8}'
    PRIOR_ROYALTY_STATUS = '[AND]'  # Matching available values [A, N, D]
    PRIOR_ROYALTY_START_DATE = '[ \d]{8}'  # Required is status is D
    POST_TERM_COLLECTION_STATUS = '[NOD]'
    POST_TERM_COLLECTION_END_DATE = '[ \d]{8}'
    SIGNATURE_DATE = '[ \d]{8}'
    WORKS_NUMBER = '\d{5}'
    SALES_CLAUSE = '[SM ]'
    SHARES_CHANGE = '[YN ]'
    ADVANCE_GIVEN = '[YN ]'
    SOCIETY_ASSIGNED_NUMBER = '[ -~]{14}'

    AGREEMENT_RECORD_REGEX = "^{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}{17}$".format(
        RECORD_TYPE, AGREEMENT_NUMBER, SUBMITTER_NUMBER, INTERNATIONAL_CODE, AGREEMENT_TYPE, START_DATE, END_DATE,
        RETENTION_END_DATE, PRIOR_ROYALTY_STATUS, PRIOR_ROYALTY_START_DATE, POST_TERM_COLLECTION_STATUS,
        POST_TERM_COLLECTION_END_DATE, SIGNATURE_DATE, WORKS_NUMBER, SALES_CLAUSE, SHARES_CHANGE, ADVANCE_GIVEN,
        SOCIETY_ASSIGNED_NUMBER)

    def __init__(self, record):
        matcher = re.compile(self.AGREEMENT_RECORD_REGEX)
        if matcher.match(record):
            self._build_agreement_record(record)
        else:
            raise ValueError('Given record: %s does not match required format' % record)

    def _build_agreement_record(self, record):
        self._number = int(record[3:3 + 8])
        self._submitter = record[19:19 + 14]
        self._international_code = record[33:33 + 14] if record[33:33 + 14] else None
        self._type = record[47:47 + 2]
        if self._type not in self.AGREEMENT_TYPE_VALUES:
            raise ValueError('Given agreement type: %s not in the required ones' % self._type)

        self._start_date = datetime.datetime.strptime(record[49:49 + 8], '%Y%m%d').date()
        if record[57:57 + 8].strip():
            self._end_date = datetime.datetime.strptime(record[57:57 + 8], '%Y%m%d').date()
        else:
            self._end_date = None

        # Not in a single line for reading purposes
        if record[65:65 + 8].strip():
            self._retention_end_date = datetime.datetime.strptime(record[65:65 + 8], '%Y%m%d').date()
        else:
            self._retention_end_date = None

        self._prior_royalty_status = record[73:73 + 1]
        if self._prior_royalty_status == 'D':
            self._prior_royalty_date = datetime.datetime.strptime(record[74:74 + 8], '%Y%m%d').date()
        elif record[74:74 + 8].strip():
            raise ValueError('Not expecting royalty date for royalty status %s' % self._prior_royalty_status)

        self._post_term_collection_stat = record[82:82 + 1]
        if self._post_term_collection_stat == 'D':
            self._post_term_collection_date = datetime.datetime.strptime(record[83:83 + 8], '%Y%m%d').date()
        elif record[83:83 + 8].strip():
            raise ValueError('Not expecting post-term collection date for status %s' % self._post_term_collection_stat)

        # Not in a single line for reading purposes
        if record[91:91 + 8].strip():
            self._signature_date = datetime.datetime.strptime(record[91:91 + 8], '%Y%m%d').date()
        else:
            self._signature_date = None

        self._works_number = int(record[99:99 + 5])

        # Sales clause is only mandatory for OS and PS agreements
        if record[104:104 + 1].strip():
            self._sales_clause = record[104:104 + 1]
        elif self._type == 'OS' or self._type == 'PS':
            raise ValueError('Sales clause not specified for an agreement type of %s' % self._type)

        self._shares_change = record[105:105 + 1] == 'T'
        self._advance_given = record[106:106 + 1] == 'T'

        self._society_assigned_number = record[107:107 + 14] if record[107:107 + 14].strip() else None

    '''@staticmethod
    def check_optional(value):
        if not value:
            return None
        return value'''

    def __str__(self):
        return 'Not implemented yet'

    def __repr__(self):
        return self.__str__()