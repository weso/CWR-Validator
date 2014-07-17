__author__ = 'Borja'
import re

from domain.records.agreement_record import AgreementRecord
from domain.records.group_header_record import GroupHeaderRecord
from domain.records.group_trailer_record import GroupTrailerRecord
from domain.records.instrumentation_summary_record import InstrumentationSummaryRecord
from domain.records.interested_party_record import InterestedPartyRecord
from domain.records.performing_artist_record import PerformingArtistRecord
from domain.records.publisher_control_record import PublisherControlRecord
from domain.records.publisher_territory_record import PublisherTerritoryRecord
from domain.records.recording_detail_record import RecordingDetailRecord
from domain.records.registration_record import RegistrationRecord
from domain.records.territory_record import TerritoryRecord
from domain.records.transmission_header_record import TransmissionHeaderRecord
from domain.records.transmission_trailer_record import TransmissionTrailerRecord
from domain.records.work_alternative_title_record import WorkAlternativeTitleRecord
from domain.records.work_origin_record import WorkOriginRecord
from domain.records.work_excerpt_title import WorkExcerptTitle
from domain.records.writer_agent_record import WriterAgentRecord
from domain.records.writer_control_record import WriterControlRecord
from domain.records.writer_territory_record import WriterTerritoryRecord


class Validator(object):
    NAME_REGEX = 'CW\d{2}\d{4}([A-Za-z_0-9]{6})\.V\d{2}'
    PREV_VERSION_NAME_REGEX = 'CW\d{2}\d{2}([A-Za-z_0-9]{6})\.V\d{2}'

    def __init__(self):
        pass

    def run(self, file_name):
        print 'Validating CWR file'
        if self.validate_name(file_name):
            self.validate_file(file_name)

    def validate_file(self, file_name):
        pass

    def validate_name(self, file_name):
        if file_name is None:
            return False

        matcher = re.compile(self.NAME_REGEX)
        if not matcher.match(file_name.upper()):
            matcher = re.compile(self.PREV_VERSION_NAME_REGEX)
            if matcher.match(file_name.upper()):
                print 'CWR file is in a previous file name convention'
            return False

        return True