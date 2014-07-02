__author__ = 'Borja'
import re

from domain.agreement_record import AgreementRecord
from domain.group_header import GroupHeader
from domain.group_trailer import GroupTrailer
from domain.ipa_record import InterestedPartyRecord
from domain.publisher_control_record import PublisherControlRecord
from domain.publisher_territory_record import PublisherTerritoryRecord
from domain.registration_record import RegistrationRecord
from domain.territory_record import TerritoryRecord
from domain.transmission_header import TransmissionHeader
from domain.transmission_trailer import TransmissionTrailer
from domain.writer_agent_record import WriterAgentRecord
from domain.writer_control_record import WriterControlRecord
from domain.writer_territory_record import WriterTerritoryRecord


class Validator(object):
    NAME_REGEX = 'CW\d{2}\d{4}([A-Za-z_0-9]{6})\.V\d{2}'
    PREV_VERSION_NAME_REGEX = 'CW\d{2}\d{2}([A-Za-z_0-9]{6})\.V\d{2}'

    NWR_RECORDS = ['PER', 'PWR', 'SPT', 'SPU', 'SWR', 'SWT']

    def __init__(self):
        self._transmission_header = None
        self._transmission_trailer = None
        self._group_headers = {}
        self._group_trailers = {}

    def run(self, file_name):
        print 'Validating CWR file'
        if self.validate_name(file_name):
            self.validate_file(file_name)

    def validate_file(self, file_name):
        with open(file_name) as file_buffer:
            file_content = file_buffer.readlines()

        if self.validate_transmission_header(file_content.pop(0)):
            while True:
                next_line = file_content.pop(0)
                if self.validate_group_header(next_line):
                    if not self.validate_group(next_line, file_content):
                        return False
                elif self.validate_transmission_trailer(next_line):
                    if len(file_content) != 0:
                        return False
                    break
                else:
                    return False

        return False

    def validate_transmission_header(self, record):
        if record is None:
            return False

        try:
            self._transmission_header = TransmissionHeader(record.upper())
            print self._transmission_header
            return True
        except ValueError as detail:
            print detail
            return False

    def validate_group_header(self, record):
        if record is None:
            return False

        try:
            group_header = GroupHeader(record.upper())
            if group_header.transaction_type not in self._group_headers.keys():
                self._group_headers[group_header.transaction_type] = group_header
                print group_header
                return True
            else:
                raise ValueError('The given transaction type: %s, has already been processed'
                                 % group_header.transaction_type)
        except ValueError as detail:
            print detail
            return False

    @staticmethod
    def validate_agreement_record(record):
        if record is None:
            return False
        try:
            AgreementRecord(record.upper())
            return True
        except ValueError as detail:
            print detail
            return False

    @staticmethod
    def validate_territory_record(record):
        if record is None:
            return False
        try:
            TerritoryRecord(record.upper())
            return True
        except ValueError as detail:
            print detail
            return False

    @staticmethod
    def validate_interested_party_record(record):
        if record is None:
            return False
        try:
            InterestedPartyRecord(record.upper())
            return True
        except ValueError as detail:
            print 'Next record didn\'t validate correctly: %s' % record
            print detail
            return False

    @staticmethod
    def validate_registration_record(record):
        if record is None:
            return False
        try:
            RegistrationRecord(record.upper())
            return True
        except ValueError as detail:
            print 'Next record didn\'t validate correctly: [%s]' % record
            print detail
            return False

    @staticmethod
    def validate_publisher_control_record(record):
        if record is None:
            return False
        try:
            PublisherControlRecord(record.upper())
            return True
        except ValueError as detail:
            print 'Next record didn\'t validate correctly: [%s]' % record
            print detail
            return False

    @staticmethod
    def validate_publisher_territory_record(record):
        if record is None:
            return False
        try:
            PublisherTerritoryRecord(record.upper())
            return True
        except ValueError as detail:
            print 'Next record didn\'t validate correctly: [%s]' % record
            print detail
            return False
    @staticmethod
    def validate_writer_agent_record(record):
        if record is None:
            return False
        try:
            WriterAgentRecord(record.upper())
            return True
        except ValueError as detail:
            print 'Next record didn\'t validate correctly: [%s]' % record
            print detail
            return False

    @staticmethod
    def validate_writer_control_record(record):
        if record is None:
            return False
        try:
            WriterControlRecord(record.upper())
            return True
        except ValueError as detail:
            print 'Next record didn\'t validate correctly: [%s]' % record
            print detail
            return False

    @staticmethod
    def validate_writer_territory_record(record):
        if record is None:
            return False
        try:
            WriterTerritoryRecord(record.upper())
            return True
        except ValueError as detail:
            print 'Next record didn\'t validate correctly: [%s]' % record
            print detail
            return False

    def validate_group_trailer(self, record):
        if record is None:
            return False

        try:
            group_trailer = GroupTrailer(record.upper())
            if group_trailer.group_id not in self._group_trailers.keys():
                self._group_trailers[group_trailer.group_id] = group_trailer
                print group_trailer
                return True
            else:
                raise ValueError('The given group: %s, has already been processed' % group_trailer.group_id)
        except ValueError as detail:
            print detail
            return False

    def validate_transmission_trailer(self, record):
        if record is None:
            return False

        try:
            self._transmission_trailer = TransmissionTrailer(record.upper())
            print self._transmission_trailer
            return True
        except ValueError as detail:
            print detail
            return False

    def validate_group(self, record, group_content):
        group_type = record[3:6]

        if group_type == 'AGR':
            return self.validate_agreement_group(group_content)
        elif group_type == 'NWR':
            return self.validate_new_work_group(group_content)
        elif group_type == 'REV':
            return self.validate_revision_group(group_content)

        print "Invalid group type (%s) for group" % group_type
        return False

    def validate_agreement_group(self, group_content):
        if self._validated_groups["AGR"]:
            print "Agreements group already validated"
            return False

        while True:
            agreement_record = group_content.pop(0)

            # May have several territories
            if agreement_record.startswith('AGR'):
                territory_record = group_content.pop(0)
                submitter_record = group_content.pop(0)
                acquirer_record = group_content.pop(0)

                if not territory_record.startswith('TER'):
                    print "Territory record \"%s\" not valid" % territory_record
                    break
                elif not submitter_record.startswith('IPA'):
                    print "Submitter record \"%s\" not valid" % submitter_record
                    break
                elif not acquirer_record.startswith('IPA'):
                    print "Acquirer record \"%s\" not valid" % acquirer_record
                    break

            elif agreement_record.startswith('GRT'):
                self._validated_groups['AGR'] = True
                return True
            else:
                print "The record \"%s\" is not valid" % agreement_record
                break

        return False

    def validate_new_work_group(self, group_content):
        if self._validated_groups['NWR']:
            return False

        next_line = group_content.pop(0)
        while True:
            if next_line.starts_with('NWR'):
                while True:
                    next_line = group_content.pop(0)
                    if next_line[0:3] == 'NWR' or next_line[0:3] == 'GRT':
                        break

                    if next_line[0:3] not in self.NWR_RECORDS:
                        return False
            elif next_line.starts_with('GRT'):
                self._validated_groups['NWR'] = True
                return True
            else:
                break

        return False

    def validate_revision_group(self, group_content):
        if self._validated_groups['REV']:
            return False

        next_line = group_content.pop(0)
        while True:
            if next_line.starts_with('REV'):
                while True:
                    next_line = group_content.pop(0)
                    if next_line[0:3] == 'REV' or next_line[0:3] == 'GRT':
                        break

                    if next_line[0:3] not in self.NWR_RECORDS:
                        return False
            elif next_line.starts_with('GRT'):
                self._validated_groups['REV'] = True
                return True
            else:
                break

        return False

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