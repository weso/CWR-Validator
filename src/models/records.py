__author__ = 'Borja'
import re

import regex
from cwr_objects import CWRField, Agreement, WorkAlternativeTitle, WorkAdditionalInfo, WorkComponent, \
    WorkExcerptTitle, Group, GroupTrailer, Header, InstrumentationDetails, InstrumentationSummary, InterestedParty, \
    NRWorkTitle, NRSpecialTitle, NROtherWriterName, NRPartyName, NRPublisherName, NRPerformanceData, NRWriterName, \
    Registration, WorkOrigin, PerformingArtist, WriterAgent, RecordingDetail, PublisherTerritory, PublisherControl, \
    WriterControl, WriterTerritory, Territory, Trailer, WorkVersionTitle


class Record(object):
    def __init__(self, record, fields):
        self.fields = fields

        if record is None or record == '':
            raise ValueError("Record can't be None")

        # Raw record identifies the record String
        self._raw_record = record

        # The final regex and the size it has
        self._regex, self._regex_size = self._generate_regex()

        # Whether a record is rejected or not
        self._rejected = False

    @staticmethod
    def factory(record):
        record_type = record[0:3]

        if record_type == 'AGR':
            record_object = AgreementRecord(record)
        elif record_type == 'ALT':
            record_object = WorkAlternativeTitleRecord(record)
        elif record_type == 'ARI':
            record_object = WorkAdditionalInfoRecord(record)
        elif record_type == 'COM':
            record_object = WorkCompositeRecord(record)
        elif record_type == 'EWT':
            record_object = WorkExcerptTitleRecord(record)
        elif record_type == 'GRH':
            record_object = GroupHeaderRecord(record)
        elif record_type == 'GRT':
            record_object = GroupTrailerRecord(record)
        elif record_type == 'HDR':
            record_object = TransmissionHeaderRecord(record)
        elif record_type == 'IND':
            record_object = InstrumentationDetailRecord(record)
        elif record_type == 'INS':
            record_object = InstrumentationSummaryRecord(record)
        elif record_type == 'IPA':
            record_object = InterestedPartyRecord(record)
        elif record_type == 'NAT':
            record_object = NRWorkTitleRecord(record)
        elif record_type in ['NCT', 'NET', 'NVT']:
            record_object = NRSpecialTitleRecord(record)
        elif record_type == 'NOW':
            record_object = NROtherWriterRecord(record)
        elif record_type == 'NPA':
            record_object = NRAgreementPartyNameRecord(record)
        elif record_type == 'NPN':
            record_object = NRPublisherNameRecord(record)
        elif record_type == 'NPR':
            record_object = NRPerformanceDataRecord(record)
        elif record_type == 'NWN':
            record_object = NRWriterNameRecord(record)
        elif record_type in ['NWR', 'REV']:
            record_object = RegistrationRecord(record)
        elif record_type == 'ORN':
            record_object = WorkOriginRecord(record)
        elif record_type == 'PER':
            record_object = PerformingArtistRecord(record)
        elif record_type == 'PWR':
            record_object = WriterAgentRecord(record)
        elif record_type == 'REC':
            record_object = RecordingDetailRecord(record)
        elif record_type == 'SPT':
            record_object = PublisherTerritoryRecord(record)
        elif record_type in ['SPU', 'OPU']:
            record_object = PublisherControlRecord(record)
        elif record_type in ['SWR', 'OWR']:
            record_object = WriterControlRecord(record)
        elif record_type == 'SWT':
            record_object = WriterTerritoryRecord(record)
        elif record_type == 'TER':
            record_object = TerritoryRecord(record)
        elif record_type == 'TRL':
            record_object = TransmissionTrailerRecord(record)
        elif record_type == 'VER':
            record_object = WorkVersionTitleRecord(record)
        else:
            raise ValueError('Wrong record creation, obtained type: {}'.format(record_type))

        return record_object

    @property
    def rejected(self):
        return self._rejected

    def promote(self, number):
        if self._extract_values():
            record_type = self.fields[0].value

            if record_type == 'AGR':
                record_object = Agreement(number, self._raw_record, self.fields)
            elif record_type == 'ALT':
                record_object = WorkAlternativeTitle(number, self._raw_record, self.fields)
            elif record_type == 'ARI':
                record_object = WorkAdditionalInfo(number, self._raw_record, self.fields)
            elif record_type == 'COM':
                record_object = WorkComponent(number, self._raw_record, self.fields)
            elif record_type == 'EWT':
                record_object = WorkExcerptTitle(number, self._raw_record, self.fields)
            elif record_type == 'GRH':
                record_object = Group(number, self._raw_record, self.fields)
            elif record_type == 'GRT':
                record_object = GroupTrailer(number, self._raw_record, self.fields)
            elif record_type == 'HDR':
                record_object = Header(number, self._raw_record, self.fields)
            elif record_type == 'IND':
                record_object = InstrumentationDetails(number, self._raw_record, self.fields)
            elif record_type == 'INS':
                record_object = InstrumentationSummary(number, self._raw_record, self.fields)
            elif record_type == 'IPA':
                record_object = InterestedParty(number, self._raw_record, self.fields)
            elif record_type == 'NAT':
                record_object = NRWorkTitle(number, self._raw_record, self.fields)
            elif record_type in ['NCT', 'NET', 'NVT']:
                record_object = NRSpecialTitle(number, self._raw_record, self.fields)
            elif record_type == 'NOW':
                record_object = NROtherWriterName(number, self._raw_record, self.fields)
            elif record_type == 'NPA':
                record_object = NRPartyName(number, self._raw_record, self.fields)
            elif record_type == 'NPN':
                record_object = NRPublisherName(number, self._raw_record, self.fields)
            elif record_type == 'NPR':
                record_object = NRPerformanceData(number, self._raw_record, self.fields)
            elif record_type == 'NWN':
                record_object = NRWriterName(number, self._raw_record, self.fields)
            elif record_type in ['NWR', 'REV']:
                record_object = Registration(number, self._raw_record, self.fields)
            elif record_type == 'ORN':
                record_object = WorkOrigin(number, self._raw_record, self.fields)
            elif record_type == 'PER':
                record_object = PerformingArtist(number, self._raw_record, self.fields)
            elif record_type == 'PWR':
                record_object = WriterAgent(number, self._raw_record, self.fields)
            elif record_type == 'REC':
                record_object = RecordingDetail(number, self._raw_record, self.fields)
            elif record_type == 'SPT':
                record_object = PublisherTerritory(number, self._raw_record, self.fields)
            elif record_type in ['SPU', 'OPU']:
                record_object = PublisherControl(number, self._raw_record, self.fields)
            elif record_type in ['SWR', 'OWR']:
                record_object = WriterControl(number, self._raw_record, self.fields)
            elif record_type == 'SWT':
                record_object = WriterTerritory(number, self._raw_record, self.fields)
            elif record_type == 'TER':
                record_object = Territory(number, self._raw_record, self.fields)
            elif record_type == 'TRL':
                record_object = Trailer(number, self._raw_record, self.fields)
            elif record_type == 'VER':
                record_object = WorkVersionTitle(number, self._raw_record, self.fields)
            else:
                raise ValueError('Wrong record promotion, obtained type: {}'.format(record_type))

            return record_object

    def check_format_with_regex(self):
        """
        Checks if a given record fulfill the regular expression requirements for it's kind
        :return: True if the regular expression matches, false otherwise
        """
        matcher = re.compile(self._regex)

        if not matcher.match(self._raw_record[0:self._regex_size]):
            self._rejected = True

        return not self._rejected

    def _extract_values(self):
        if not self.check_format_with_regex():
            return False

        start = 0

        for field in self.fields:
            field.value = self._get_value(start, field.regular_expression.size)
            start += field.regular_expression.size

        return True

    def _generate_regex(self):
        """
        Compose the regular expression, as well as it's size
        :return: The composed regular expression, The size of it
        """
        regex_string = '^' + "".join(str(field.regular_expression) for field in self.fields) + '$'
        regex_size = sum(field.regular_expression.size for field in self.fields)

        return regex_string, regex_size

    def _get_value(self, starts, size):
        value = self._raw_record[starts:starts + size].strip().encode('utf-8')

        return str(value) if value else None

    def __str__(self):
        return self._raw_record

    def __repr__(self):
        return self.__str__()


class SocietyAffiliation(object):
    REGEX = regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True) + regex.get_numeric_regex(1, True)


class AgreementRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'AGR')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Submitter number', regex.get_alphanumeric_regex(14)),
                  CWRField('International standard number', regex.get_alphanumeric_regex(14, True)),
                  CWRField('Type', regex.get_alpha_regex(2)),
                  CWRField('Start date', regex.get_date_regex()),
                  CWRField('End date', regex.get_date_regex(True)),
                  CWRField('Retention end date', regex.get_date_regex(True)),
                  CWRField('Prior royalty status', regex.get_defined_values_regex(1, False, 'A', 'D', 'N')),
                  CWRField('Prior royalty status date', regex.get_date_regex(True)),
                  CWRField('Post_term collection status', regex.get_defined_values_regex(1, False, 'D', 'N', 'O')),
                  CWRField('Post_term collection end date', regex.get_date_regex(True)),
                  CWRField('Signature date', regex.get_date_regex(True)),
                  CWRField('Works number', regex.get_numeric_regex(5)),
                  CWRField('Sales Manufacture clause', regex.get_defined_values_regex(1, True, 'N', 'S')),
                  CWRField('Shares change', regex.get_boolean_regex(True)),
                  CWRField('Advance given', regex.get_boolean_regex(True)),
                  CWRField('Society assigned number', regex.get_alphanumeric_regex(14, True))]

        super(AgreementRecord, self).__init__(record, fields)


class GroupHeaderRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'GRH')),
                  CWRField('Transaction type', regex.get_defined_values_regex(3, False, 'AGR', 'NWR', 'REV')),
                  CWRField('ID', regex.get_numeric_regex(5)),
                  CWRField('Transaction type version number', regex.get_defined_values_regex(5, False, '02\.10')),
                  CWRField('Batch request', regex.get_numeric_regex(10, True)),
                  CWRField('Submission Distribution type', regex.get_optional_regex(2))]

        super(GroupHeaderRecord, self).__init__(record, fields)


class GroupTrailerRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'GRT')),
                  CWRField('Group ID', regex.get_numeric_regex(5)),
                  CWRField('Transaction count', regex.get_numeric_regex(8)),
                  CWRField('Record count', regex.get_numeric_regex(8)),
                  CWRField('Currency indicator', regex.get_alpha_regex(3, True)),
                  CWRField('Total monetary value', regex.get_numeric_regex(10, True))]

        super(GroupTrailerRecord, self).__init__(record, fields)


class InstrumentationDetailRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'IND')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Instrument code', regex.get_alpha_regex(3)),
                  CWRField('Players number', regex.get_numeric_regex(3, True))]

        super(InstrumentationDetailRecord, self).__init__(record, fields)


class InstrumentationSummaryRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'INS')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Voices number', regex.get_numeric_regex(3, True)),
                  CWRField('Standard instrumentation type', regex.get_ascii_regex(3, True)),
                  CWRField('Instrumentation description', regex.get_ascii_regex(50, True))]

        super(InstrumentationSummaryRecord, self).__init__(record, fields)


class InterestedPartyRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'IPA')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Agreement role code', regex.get_alpha_regex(2)),
                  CWRField('CAE IPI ID', regex.get_ascii_regex(11, True)),
                  CWRField('IPI base number', regex.get_numeric_regex(13, True)),
                  CWRField('ID', regex.get_ascii_regex(9)),
                  CWRField('Last name', regex.get_ascii_regex(45)),
                  CWRField('Writer first name', regex.get_ascii_regex(30, True)),
                  CWRField('PR society', SocietyAffiliation.REGEX),
                  CWRField('PR share', regex.get_numeric_regex(5)),
                  CWRField('MR society', SocietyAffiliation.REGEX),
                  CWRField('MR share', regex.get_numeric_regex(5)),
                  CWRField('SR society', SocietyAffiliation.REGEX),
                  CWRField('SR share', regex.get_numeric_regex(5))]

        super(InterestedPartyRecord, self).__init__(record, fields)


class NRAgreementPartyNameRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'NPA')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Interested party ID', regex.get_ascii_regex(9)),
                  CWRField('Name', regex.get_non_roman_regex(160)),
                  CWRField('Writer first name', regex.get_non_roman_regex(160)),
                  CWRField('Language code', regex.get_alpha_regex(2, True))]

        super(NRAgreementPartyNameRecord, self).__init__(record, fields)


class NROtherWriterRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'NOW')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Writer name', regex.get_ascii_regex(160)),
                  CWRField('Writer first name', regex.get_ascii_regex(160)),
                  CWRField('Language code', regex.get_alpha_regex(2, True)),
                  CWRField('Writer position', regex.get_alpha_regex(1, True))]

        super(NROtherWriterRecord, self).__init__(record, fields)


class NRPerformanceDataRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'NPR')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Artist name', regex.get_ascii_regex(160, True)),
                  CWRField('Artist first name', regex.get_ascii_regex(160, True)),
                  CWRField('Artist IPI CAE ID', regex.get_ascii_regex(11, True)),
                  CWRField('Artist IPI base number', regex.get_ascii_regex(13, True)),
                  CWRField('Language code', regex.get_alpha_regex(2, True)),
                  CWRField('Performance language', regex.get_alpha_regex(2, True)),
                  CWRField('Performance dialect', regex.get_alpha_regex(3, True))]

        super(NRPerformanceDataRecord, self).__init__(record, fields)


class NRPublisherNameRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'NPN')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Publisher sequence ID', regex.get_numeric_regex(2)),
                  CWRField('Interested party ID', regex.get_ascii_regex(9)),
                  CWRField('Publisher name', regex.get_ascii_regex(480)),
                  CWRField('Language code', regex.get_alpha_regex(2, True))]

        super(NRPublisherNameRecord, self).__init__(record, fields)


class NRSpecialTitleRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'NET', 'NCT', 'NVT')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Title', regex.get_ascii_regex(640)),
                  CWRField('Language code', regex.get_alpha_regex(2, True))]

        super(NRSpecialTitleRecord, self).__init__(record, fields)


class NRWorkTitleRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'NPN')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Title', regex.get_ascii_regex(640)),
                  CWRField('Title type', regex.get_ascii_regex(2)),
                  CWRField('Language code', regex.get_alpha_regex(2, True))]

        super(NRWorkTitleRecord, self).__init__(record, fields)


class NRWriterNameRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'NWR')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Interested party ID', regex.get_ascii_regex(9)),
                  CWRField('Writer name', regex.get_ascii_regex(160)),
                  CWRField('Writer first name', regex.get_ascii_regex(160)),
                  CWRField('Language code', regex.get_alpha_regex(2, True))]

        super(NRWriterNameRecord, self).__init__(record, fields)


class PerformingArtistRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'PER')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Last name', regex.get_ascii_regex(45)),
                  CWRField('First name', regex.get_ascii_regex(30, True)),
                  CWRField('CAE IPI name', regex.get_ascii_regex(11, True)),
                  CWRField('IPI base number', regex.get_ascii_regex(13, True))]

        super(PerformingArtistRecord, self).__init__(record, fields)


class PublisherControlRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'OPU', 'SPU')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Sequence ID', regex.get_numeric_regex(2)),
                  CWRField('Interested party ID', regex.get_ascii_regex(9, True)),
                  CWRField('Name', regex.get_ascii_regex(45, True)),
                  CWRField('Unknown indicator', regex.get_flag_regex(True)),
                  CWRField('Type', regex.get_alpha_regex(1, True) + regex.get_alpha_regex(1, True)),
                  CWRField('Tax ID number', regex.get_ascii_regex(9, True)),
                  CWRField('CAE IPI name', regex.get_numeric_regex(11, True)),
                  CWRField('Agreement number', regex.get_ascii_regex(14, True)),
                  CWRField('PR society', SocietyAffiliation.REGEX),
                  CWRField('PR share', regex.get_numeric_regex(5, True)),
                  CWRField('MR society', SocietyAffiliation.REGEX),
                  CWRField('MR share', regex.get_numeric_regex(5, True)),
                  CWRField('SR society', SocietyAffiliation.REGEX),
                  CWRField('SR share', regex.get_numeric_regex(5, True)),
                  CWRField('Reversionary_indicator', regex.get_flag_regex(True)),
                  CWRField('First recording refusal indicator', regex.get_flag_regex(True)),
                  CWRField('Filler', regex.get_optional_regex(1)),
                  CWRField('IPI base number', regex.get_ascii_regex(13, True)),
                  CWRField('International standard agreement code', regex.get_ascii_regex(14, True)),
                  CWRField('Society assigned agreement number', regex.get_ascii_regex(14, True)),
                  CWRField('Agreement type', regex.get_alpha_regex(2, True)),
                  CWRField('USA licensed indicator', regex.get_alpha_regex(1, True))]

        super(PublisherControlRecord, self).__init__(record, fields)


class PublisherTerritoryRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'SPT')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Interested party ID', regex.get_ascii_regex(9)),
                  CWRField('Constant', regex.get_optional_regex(6)),
                  CWRField('PR share', regex.get_numeric_regex(5, True)),
                  CWRField('MR share', regex.get_numeric_regex(5, True)),
                  CWRField('SR share', regex.get_numeric_regex(5, True)),
                  CWRField('Inclusion exclusion indicator', regex.get_defined_values_regex(1, False, 'E', 'I')),
                  CWRField('TIS numeric code', regex.get_numeric_regex(4)),
                  CWRField('Shares change', regex.get_boolean_regex()),
                  CWRField('Sequence ID', regex.get_numeric_regex(3))]

        super(PublisherTerritoryRecord, self).__init__(record, fields)


class RecordingDetailRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'REC')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('First release date', regex.get_date_regex(True)),
                  CWRField('Constant', regex.get_optional_regex(60)),
                  CWRField('First release duration', regex.get_time_regex(True)),
                  CWRField('Constant', regex.get_optional_regex(5)),
                  CWRField('First album title', regex.get_ascii_regex(60, True)),
                  CWRField('First album label', regex.get_ascii_regex(60, True)),
                  CWRField('First release catalog ID', regex.get_ascii_regex(18, True)),
                  CWRField('EAN', regex.get_ascii_regex(13, True)),
                  CWRField('ISRC', regex.get_ascii_regex(12, True)),
                  CWRField('Recording format', regex.get_alpha_regex(1, True)),
                  CWRField('Recording technique', regex.get_alpha_regex(1, True)),
                  CWRField('Media type', regex.get_ascii_regex(3, True))]

        super(RecordingDetailRecord, self).__init__(record, fields)


class RegistrationRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'NWR', 'REV')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Title', regex.get_ascii_regex(60)),
                  CWRField('Language code', regex.get_alpha_regex(2, True)),
                  CWRField('Submitter ID', regex.get_ascii_regex(14)),
                  CWRField('ISWC', regex.get_ascii_regex(11, True)),
                  CWRField('Copyright date', regex.get_date_regex(True)),
                  CWRField('Copyright number', regex.get_ascii_regex(12, True)),
                  CWRField('Musical distribution category', regex.get_alpha_regex(3)),
                  CWRField('Duration', regex.get_time_regex(True)),
                  CWRField('Recorded indicator', regex.get_flag_regex()),
                  CWRField('Text music relationship', regex.get_alpha_regex(3, True)),
                  CWRField('Composite type', regex.get_alpha_regex(3, True)),
                  CWRField('Version type', regex.get_alpha_regex(3)),
                  CWRField('Excerpt type', regex.get_alpha_regex(3, True)),
                  CWRField('Music arrangement', regex.get_alpha_regex(3, True)),
                  CWRField('Lyric adaptation', regex.get_alpha_regex(3, True)),
                  CWRField('Contact name', regex.get_ascii_regex(30, True)),
                  CWRField('Contact ID', regex.get_ascii_regex(10, True)),
                  CWRField('CWR work type', regex.get_alpha_regex(2, True)),
                  CWRField('Grand rights indicator', regex.get_boolean_regex(True)),
                  CWRField('Composite component count', regex.get_numeric_regex(3, True)),
                  CWRField('Printed edition publication date', regex.get_date_regex(True)),
                  CWRField('Exceptional clause', regex.get_flag_regex(True)),
                  CWRField('Opus number', regex.get_ascii_regex(25, True)),
                  CWRField('Catalogue number', regex.get_ascii_regex(25, True)),
                  CWRField('Priority flag', regex.get_flag_regex(True))]

        super(RegistrationRecord, self).__init__(record, fields)


class TerritoryRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'TER')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Inclusion exclusion indicator', regex.get_defined_values_regex(1, False, 'E', 'I')),
                  CWRField('TIS numeric code', regex.get_numeric_regex(4))]

        super(TerritoryRecord, self).__init__(record, fields)


class TransmissionHeaderRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'HDR')),
                  CWRField('Sender type', regex.get_alpha_regex(2)),
                  CWRField('Sender ID', regex.get_numeric_regex(9)),
                  CWRField('Sender name', regex.get_ascii_regex(45)),
                  CWRField('EDI standard version number', regex.get_defined_values_regex(5, False, '01\.10')),
                  CWRField('Creation date', regex.get_date_regex()),
                  CWRField('Creation time', regex.get_time_regex()),
                  CWRField('Transmission date', regex.get_date_regex()),
                  CWRField('Character set', regex.get_alphanumeric_regex(15, True))]

        super(TransmissionHeaderRecord, self).__init__(record, fields)


class TransmissionTrailerRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'TRL')),
                  CWRField('Group count', regex.get_numeric_regex(5)),
                  CWRField('Transaction count', regex.get_numeric_regex(8)),
                  CWRField('Record count', regex.get_numeric_regex(8))]

        super(TransmissionTrailerRecord, self).__init__(record, fields)


class WorkAdditionalInfoRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'TER')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Society ID', regex.get_numeric_regex(3)),
                  CWRField('Work ID', regex.get_ascii_regex(14, True)),
                  CWRField('Right type', regex.get_alpha_regex(3)),
                  CWRField('Subject code', regex.get_alpha_regex(2, True)),
                  CWRField('Note', regex.get_ascii_regex(160, True))]

        super(WorkAdditionalInfoRecord, self).__init__(record, fields)


class WorkAlternativeTitleRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'ALT')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Alternate title', regex.get_non_roman_regex(60)),
                  CWRField('Title type', regex.get_alpha_regex(2)),
                  CWRField('Language code', regex.get_alpha_regex(2, True))]

        super(WorkAlternativeTitleRecord, self).__init__(record, fields)


class WorkCompositeRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'COM')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Title', regex.get_ascii_regex(60)),
                  CWRField('ISWC', regex.get_ascii_regex(11, True)),
                  CWRField('Submitter ID', regex.get_ascii_regex(14, True)),
                  CWRField('Duration', regex.get_time_regex(True)),
                  CWRField('Writer one last name', regex.get_ascii_regex(45)),
                  CWRField('Writer one first name', regex.get_ascii_regex(30, True)),
                  CWRField('Writer one ipi cae', regex.get_numeric_regex(11, True)),
                  CWRField('Writer two last name', regex.get_ascii_regex(45)),
                  CWRField('Writer two first name', regex.get_ascii_regex(30, True)),
                  CWRField('Writer two ipi cae', regex.get_numeric_regex(11, True)),
                  CWRField('Writer one ipi base number', regex.get_numeric_regex(13, True)),
                  CWRField('Writer two ipi base number', regex.get_numeric_regex(13, True))]

        super(WorkCompositeRecord, self).__init__(record, fields)


class WorkExcerptTitleRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'EWT')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Entire title', regex.get_ascii_regex(60)),
                  CWRField('Entire work ISWC', regex.get_ascii_regex(11, True)),
                  CWRField('Language code', regex.get_alpha_regex(2, True)),
                  CWRField('Writer one last name', regex.get_ascii_regex(45)),
                  CWRField('Writer one first name', regex.get_ascii_regex(30, True)),
                  CWRField('Source', regex.get_ascii_regex(60, True)),
                  CWRField('Writer one ipi cae', regex.get_numeric_regex(11, True)),
                  CWRField('Writer one ipi base number', regex.get_numeric_regex(13, True)),
                  CWRField('Writer two last name', regex.get_ascii_regex(45)),
                  CWRField('Writer two first name', regex.get_ascii_regex(30, True)),
                  CWRField('Writer two ipi cae', regex.get_numeric_regex(11, True)),
                  CWRField('Writer two ipi base number', regex.get_numeric_regex(13, True)),
                  CWRField('Submitter ID', regex.get_ascii_regex(14, True))]

        super(WorkExcerptTitleRecord, self).__init__(record, fields)


class WorkOriginRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'ORN')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Intended purpose', regex.get_ascii_regex(3)),
                  CWRField('Production title', regex.get_ascii_regex(60, True)),
                  CWRField('CD identifier', regex.get_ascii_regex(15, True)),
                  CWRField('Cut number', regex.get_numeric_regex(4, True)),
                  CWRField('Library', regex.get_ascii_regex(60, True)),
                  CWRField('BLT', regex.get_ascii_regex(1, True)),
                  CWRField('Visan version', regex.get_numeric_regex(8, True)),
                  CWRField('Visan isan', regex.get_numeric_regex(12, True)),
                  CWRField('Visan episode', regex.get_numeric_regex(4, True)),
                  CWRField('Visan check digit', regex.get_numeric_regex(1, True)),
                  CWRField('Production ID', regex.get_ascii_regex(12, True)),
                  CWRField('Episode title', regex.get_ascii_regex(60, True)),
                  CWRField('Episode ID', regex.get_ascii_regex(20, True)),
                  CWRField('Production year', regex.get_numeric_regex(4, True)),
                  CWRField('AVI key society', regex.get_numeric_regex(3, True)),
                  CWRField('AVI key number', regex.get_ascii_regex(15, True))]

        super(WorkOriginRecord, self).__init__(record, fields)


class WorkVersionTitleRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'VER')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Entire title', regex.get_ascii_regex(60)),
                  CWRField('Entire work ISWC', regex.get_ascii_regex(11, True)),
                  CWRField('Language code', regex.get_alpha_regex(2, True)),
                  CWRField('Writer one last name', regex.get_ascii_regex(45)),
                  CWRField('Writer one first name', regex.get_ascii_regex(30, True)),
                  CWRField('Source', regex.get_ascii_regex(60, True)),
                  CWRField('Writer one ipi cae', regex.get_numeric_regex(11, True)),
                  CWRField('Writer one ipi base number', regex.get_numeric_regex(13, True)),
                  CWRField('Writer two last name', regex.get_ascii_regex(45)),
                  CWRField('Writer two first name', regex.get_ascii_regex(30, True)),
                  CWRField('Writer two ipi cae', regex.get_numeric_regex(11, True)),
                  CWRField('Writer two ipi base number', regex.get_numeric_regex(13, True)),
                  CWRField('Submitter ID', regex.get_ascii_regex(14, True))]

        super(WorkVersionTitleRecord, self).__init__(record, fields)


class WriterAgentRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'PWR')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('IP ID', regex.get_ascii_regex(9)),
                  CWRField('Name', regex.get_ascii_regex(45)),
                  CWRField('Agreement number', regex.get_ascii_regex(14, True)),
                  CWRField('Society assigned number', regex.get_ascii_regex(14, True)),
                  CWRField('Writer IP ID', regex.get_ascii_regex(9))]

        super(WriterAgentRecord, self).__init__(record, fields)


class WriterControlRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'OWR', 'SWR')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Interested party ID', regex.get_ascii_regex(9, True)),
                  CWRField('Last name', regex.get_ascii_regex(45, True)),
                  CWRField('First name', regex.get_ascii_regex(30, True)),
                  CWRField('Unknown indicator', regex.get_flag_regex(True)),
                  CWRField('Designation code', regex.get_alpha_regex(1, True) + regex.get_alpha_regex(1, True)),
                  CWRField('Tax ID number', regex.get_ascii_regex(9, True)),
                  CWRField('CAE IPI name ID', regex.get_numeric_regex(11, True)),
                  CWRField('PR society', SocietyAffiliation.REGEX),
                  CWRField('PR share', regex.get_numeric_regex(5, True)),
                  CWRField('MR society', SocietyAffiliation.REGEX),
                  CWRField('MR share', regex.get_numeric_regex(5, True)),
                  CWRField('SR society', SocietyAffiliation.REGEX),
                  CWRField('SR share', regex.get_numeric_regex(5, True)),
                  CWRField('Reversionary indicator', regex.get_flag_regex(True)),
                  CWRField('First recording refusal indicator', regex.get_boolean_regex(True)),
                  CWRField('Work for hire indicator', regex.get_boolean_regex(True)),
                  CWRField('Filler', regex.get_optional_regex(1)),
                  CWRField('IPI base number', regex.get_ascii_regex(13, True)),
                  CWRField('Personal number', regex.get_numeric_regex(12, True)),
                  CWRField('USA license indicator', regex.get_alpha_regex(1, True))]

        super(WriterControlRecord, self).__init__(record, fields)


class WriterTerritoryRecord(Record):
    def __init__(self, record):
        fields = [CWRField('Record type', regex.get_defined_values_regex(3, False, 'SWT')),
                  CWRField('Transaction number', regex.get_numeric_regex(8)),
                  CWRField('Record number', regex.get_numeric_regex(8)),
                  CWRField('Interested party ID', regex.get_ascii_regex(9)),
                  CWRField('PR share', regex.get_numeric_regex(5, True)),
                  CWRField('MR share', regex.get_numeric_regex(5, True)),
                  CWRField('SR share', regex.get_numeric_regex(5, True)),
                  CWRField('Inclusion exclusion indicator', regex.get_defined_values_regex(1, False, 'E', 'I')),
                  CWRField('TIS numeric code', regex.get_numeric_regex(4)),
                  CWRField('Shares change', regex.get_boolean_regex()),
                  CWRField('Sequence ID', regex.get_numeric_regex(3))]

        super(WriterTerritoryRecord, self).__init__(record, fields)