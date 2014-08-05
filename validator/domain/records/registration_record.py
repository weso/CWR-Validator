from validator.cwr_utils.value_tables import COMPOSITE_TYPE
from validator.cwr_utils.value_tables import DISTRIBUTION_CATEGORY_TABLE
from validator.cwr_utils.value_tables import EXCERPT_TYPE
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.cwr_utils.value_tables import LYRIC_ADAPTATION
from validator.cwr_utils.value_tables import MUSIC_ARRANGEMENT_TYPES
from validator.cwr_utils.value_tables import TEXT_MUSIC_TABLE
from validator.cwr_utils.value_tables import VERSION_TYPES
from validator.cwr_utils.value_tables import WORK_TYPES
from validator.cwr_utils import regex
from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.exceptions.transaction_rejected_error import TransactionRejectedError
from validator.domain.records.record import Record
from validator.domain.records.transaction_header_record import TransactionHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'


class RegistrationRecord(TransactionHeader):
    CHAIN_ORDER = ['SPU', 'NPN', 'SPT', 'OPU', 'NPN', 'SWR', 'NWN', 'SWT', 'PWR', 'OWR', 'NWN', 'ALT', 'NAT', 'EWT',
                   'NET', 'NOW', 'VER', 'NVT', 'NOW', 'PER', 'NPR', 'REC', 'ORN', 'INS', 'IND', 'COM', 'NCT', 'NOW',
                   'ARI']

    FIELD_NAMES = ['Record prefix', 'Work title', 'Language code', 'Submitter work ID', 'ISWC', 'Copyright date',
                   'Copyright number', 'Musical work distribution category', 'Duration', 'Recorded indicator',
                   'Text music relationship', 'Composite type', 'Version type', 'Excerpt type', 'Music arrangement',
                   'Lyric adaptation', 'Contact name', 'Contact ID', 'CWR work type', 'Grand rights indicator',
                   'Composite component count', 'Date of publication of printed edition', 'Exceptional clause',
                   'Opus number', 'Catalogue number', 'Priority flag']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(60), regex.get_alpha_regex(2, True),
                   regex.get_ascii_regex(14), regex.get_ascii_regex(11, True), regex.get_date_regex(True),
                   regex.get_ascii_regex(12, True), regex.get_alpha_regex(3), regex.get_time_regex(True),
                   regex.get_flag_regex(), regex.get_alpha_regex(3, True), regex.get_alpha_regex(3, True),
                   regex.get_alpha_regex(3), regex.get_alpha_regex(3, True), regex.get_alpha_regex(3, True),
                   regex.get_alpha_regex(3, True), regex.get_ascii_regex(30, True), regex.get_ascii_regex(10, True),
                   regex.get_alpha_regex(2, True), regex.get_boolean_regex(True), regex.get_numeric_regex(3, True),
                   regex.get_date_regex(True), regex.get_flag_regex(True), regex.get_ascii_regex(25, True),
                   regex.get_ascii_regex(25, True), regex.get_flag_regex(True)]

    def __init__(self, record):
        super(RegistrationRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_date_value('Copyright date')
        self.format_time_value('Duration')
        self.format_integer_value('Composite component count')
        self.format_date_value('Date of publication of printed edition')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type not in ['NWR', 'REV']:
            raise RecordRejectedError('NWR or REV record type expected', self._record, 'Record prefix')

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            raise TransactionRejectedError(self, 'Given language code not in table', self._record, 'Language code')

        if self.attr_dict['Musical work distribution category'] not in DISTRIBUTION_CATEGORY_TABLE:
            raise TransactionRejectedError(self, 'Given distribution category not in table', self._record,
                                           'Musical work distribution category')

        if self.attr_dict['Duration'] is None and self.attr_dict['Musical work distribution category'] in ['JAZ',
                                                                                                           'SER']:
            raise TransactionRejectedError(self, 'Expected duration for given work distribution', self._record,
                                           'Duration')

        if self.attr_dict['Text music relationship'] is not None and \
                self.attr_dict['Text music relationship'] not in TEXT_MUSIC_TABLE:
            raise FieldRejectedError('Given text music relationship not in table', self._record,
                                     'Text music relationship')

        if self.attr_dict['Composite type'] is not None:
            if self.attr_dict['Composite type'] not in COMPOSITE_TYPE:
                raise FieldRejectedError('Given composite type not in table', self._record, 'Composite type')
            if self.attr_dict['Composite component count'] is None or self.attr_dict['Composite component count'] <= 1:
                raise TransactionRejectedError(self, 'Expected component count', self._record,
                                               'Composite component count')
        elif self.attr_dict['Composite component count'] is not None:
            raise TransactionRejectedError(self, 'Expected composite type', self._record, 'Composite type')

        if self.attr_dict['Version type'] not in VERSION_TYPES:
            raise TransactionRejectedError(self, 'Given version type not in table', self._record, 'Version type')

        if self.attr_dict['Excerpt type'] is not None and self.attr_dict['Excerpt type'] not in EXCERPT_TYPE:
            raise FieldRejectedError('Given excerpt type not in table', self._record, 'Excerpt type')

        if self.attr_dict['Version type'] == 'MOD':
            if self.attr_dict['Music arrangement'] is not None:
                    if self.attr_dict['Music arrangement'] not in MUSIC_ARRANGEMENT_TYPES:
                        raise TransactionRejectedError(self, 'Given music arrangement not in table',
                                                       self._record, 'Music arrangement')
            else:
                raise TransactionRejectedError(self, 'Music arrangement must be entered',
                                               self._record, 'Music arrangement')

            if self.attr_dict['Lyric adaptation'] is not None:
                if self.attr_dict['Lyric adaptation'] not in LYRIC_ADAPTATION:
                    raise TransactionRejectedError(self, 'Given lyric adaptation not in table',
                                                   self._record, 'Lyric adaptation')
                else:
                    raise TransactionRejectedError(self, 'Lyric adaptation must be entered',
                                                   self._record, 'Lyric adaptation')

        if self.attr_dict['CWR work type'] is not None and self.attr_dict['CWR work type'] not in WORK_TYPES:
            self.attr_dict['CWR work type'] = None
            raise FieldRejectedError('Expected a valid number', self._record, 'CWR work type')

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError('Expected a record object, not the string')

        if record.attr_dict['Record prefix'].record_type not in self.CHAIN_ORDER:
            raise TransactionRejectedError(self, 'Trying to add a non compatible record type', record, 'Record type')

        if record.attr_dict['Record prefix'].record_type in ['EWT', 'NET', 'VER', 'NVT', 'REC']:
            if record.attr_dict['Record prefix'].record_type in self._records.keys():
                raise TransactionRejectedError(self, 'Record used more than its specified max use', record,
                                               'Record type')

        if record.attr_dict['Record prefix'].record_type in ['SPU', 'OPU'] \
                and record.attr_dict['Record prefix'].record_type not in self._records.keys():
            if record.attr_dict['Publisher type'] not in ['E', 'PA']:
                raise TransactionRejectedError(self,
                                               'First SPU or OPU within a chain must have E or PA as publisher type',
                                               record,
                                               'Publisher type')
        elif record.attr_dict['Record prefix'].record_type == 'OPU' \
                and self._records[record.attr_dict['Record prefix'].record_type].attr_dict[
                    'Record prefix'].record_number + 1 != record.attr_dict['Record prefix'].record_number:
            raise TransactionRejectedError(self, 'SPU and OPU record expected to be a chain', record)

        if record.attr_dict['Record prefix'].record_type in ['EWT', 'VER', 'REC'] and \
                record.attr_dict['Record prefix'].record_type in self._records.keys():
            raise TransactionRejectedError(self, 'Only one record of this type allowed per transaction', record)

        if record.attr_dict['Record prefix'].record_type == 'COM' and self.attr_dict['Composite type'] is None:
            raise RecordRejectedError('Expected value', self._record, 'Record prefix')

        if record.attr_dict['Record prefix'].record_type not in self._records.keys():
            self._records[record.attr_dict['Record prefix'].record_type] = []

        self._records[record.attr_dict['Record prefix'].record_type].append(record)

    def _validate_field(self, field_name):
        if field_name == 'Work title':
            raise TransactionRejectedError(self, 'Work title must be entered', self._record, field_name)
        elif field_name in ['Copyright date', 'Date of publication of printed version']:
            self.attr_dict[field_name] = None
            raise FieldRejectedError('Expected a valid date', self._record, field_name)
        elif field_name == 'ISWC':
            self.attr_dict[field_name] = None
            raise FieldRejectedError('Expected a valid ISWC', self._record, field_name)
        elif field_name == 'Duration':
            raise TransactionRejectedError('Expected a valid duration', self._record, field_name)
        elif field_name == 'Recorded indicator':
            self.attr_dict[field_name] = 'U'
            raise FieldRejectedError('Expected a valid flag', self._record, field_name)
        elif field_name == 'Grand rights':
            self.attr_dict[field_name] = None
            raise FieldRejectedError('Expected a valid boolean', self._record, field_name)
        elif field_name == 'CWR work type':
            self.attr_dict[field_name] = None
            raise FieldRejectedError('Expected a valid number', self._record, field_name)

    def validate_transaction(self):
        if self.attr_dict['Musical work distribution category'] == 'SER' and 'INS' not in self._records.keys():
            raise TransactionRejectedError(self, 'The transaction must include an instrumentation summary record')

        self._check_shares()
        self._check_writers()

    def _check_shares(self):
        publisher_pr_share = 0
        publisher_mr_share = 0
        publisher_sr_share = 0

        if 'SPU' in self._records.keys():
            for publisher in self._records['SPU']:
                publisher_pr_share += publisher.attr_dict['PR ownership share']
                publisher_mr_share += publisher.attr_dict['MR ownership share']
                publisher_sr_share += publisher.attr_dict['SR ownership share']
        if 'OPU' in self._records.keys():
            for publisher in self._records['OPU']:
                publisher_pr_share += publisher.attr_dict['PR ownership share']
                publisher_mr_share += publisher.attr_dict['MR ownership share']
                publisher_sr_share += publisher.attr_dict['SR ownership share']

        if publisher_pr_share > 50:
            raise TransactionRejectedError(self, 'PR share exceeds a 50%')
        elif publisher_mr_share > 100:
            raise TransactionRejectedError(self, 'MR share exceeds a 100%')
        elif publisher_sr_share > 100:
            raise TransactionRejectedError(self, 'SR share exceeds a 100%')

        writer_pr_share = 0
        writer_mr_share = 0
        writer_sr_share = 0

        if 'SWR' in self._records.keys():
            for writer in self._records['SWR']:
                writer_pr_share += writer.attr_dict['PR ownership share']
                writer_mr_share += writer.attr_dict['MR ownership share']
                writer_sr_share += writer.attr_dict['SR ownership share']
        if 'OWR' in self._records.keys():
            for writer in self._records['OWR']:
                writer_pr_share += writer.attr_dict['PR ownership share']
                writer_mr_share += writer.attr_dict['MR ownership share']
                writer_sr_share += writer.attr_dict['SR ownership share']

        if writer_pr_share < 50:
            raise TransactionRejectedError(self, 'PR share is less than 50%')
        elif writer_mr_share > 100:
            raise TransactionRejectedError(self, 'MR share exceeds a 100%')
        elif writer_sr_share > 100:
            raise TransactionRejectedError(self, 'SR share exceeds a 100%')

        if 0 < publisher_pr_share + writer_pr_share < 100:
            raise TransactionRejectedError(self, 'Total pr ownerships shares must be 0 or 100, obtained {}'.format(
                publisher_pr_share + writer_pr_share))
        if 0 < publisher_mr_share + writer_mr_share < 100:
            raise TransactionRejectedError(self, 'Total mr ownerships shares must be 0 or 100, obtained {}'.format(
                publisher_mr_share + writer_mr_share))
        if 0 < publisher_sr_share + writer_sr_share < 100:
            raise TransactionRejectedError(self, 'Total sr ownerships shares must be 0 or 100, obtained {}'.format(
                publisher_sr_share + writer_sr_share))

    def _check_writers(self):
        if 'SWR' not in self._records.keys() and 'OWR' not in self._records.keys():
            raise TransactionRejectedError(self, 'Expected at least one SWR or OWR record')

        modifier = False
        non_original = False
        writer = False
        expected_modifier = ['AR', 'AD', 'SR', 'SA', 'TR']
        expected_writer = ['CA', 'A', 'C']
        expected_version = ['AR', 'AD', 'TR']
        if 'SWR' in self._records.keys():
            for writer in self._records['SWR']:
                if writer.attr_dict['Writer designation code'] in expected_modifier:
                    modifier = True
                    if writer.attr_dict['Writer designation code'] in expected_version:
                        non_original = True
                elif writer.attr_dict['Writer designation code'] in expected_writer:
                    writer = True

                if writer and modifier and non_original:
                    break
        if 'OWR' in self._records.keys() and not modifier:
            for writer in self._records['OWR']:
                if writer.attr_dict['Writer designation code'] in expected_modifier:
                    modifier = True
                    if writer.attr_dict['Writer designation code'] in expected_version:
                        non_original = True
                elif writer.attr_dict['Writer designation code'] in expected_writer:
                    writer = True

                if writer and modifier and non_original:
                    break

        if not writer:
            raise TransactionRejectedError(self, 'Expected at least one writer in the work')

        if self._attr_dict['Version type'] == 'MOD' and not modifier:
            raise TransactionRejectedError(self, 'Not found expected writer designation code for mod versions')
        if self._attr_dict['Version type'] == 'ORI' and non_original:
            raise TransactionRejectedError(self, 'Found non original writer to original work')