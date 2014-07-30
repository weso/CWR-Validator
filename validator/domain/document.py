from validator.domain.exceptions.document_validation_error import DocumentValidationError
from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.exceptions.file_rejected_error import FileRejectedError
from validator.domain.exceptions.group_rejected_error import GroupRejectedError
from validator.domain.exceptions.regex_error import RegexError
from validator.domain.exceptions.transaction_rejected_error import TransactionRejectedError
from validator.domain.records.agreement_record import AgreementRecord
from validator.domain.records.group_header_record import GroupHeaderRecord
from validator.domain.records.group_trailer_record import GroupTrailerRecord
from validator.domain.records.instrumentation_detail_record import InstrumentationDetailRecord
from validator.domain.records.instrumentation_summary_record import InstrumentationSummaryRecord
from validator.domain.records.interested_party_record import InterestedPartyRecord
from validator.domain.records.nr_agreement_party_name_record import NRAgreementPartyNameRecord
from validator.domain.records.nr_other_writer_record import NROtherWriterRecord
from validator.domain.records.nr_performance_data_record import NRPerformanceDataRecord
from validator.domain.records.nr_publisher_name_record import NRPublisherNameRecord
from validator.domain.records.nr_special_title_record import NRSpecialTitleRecord
from validator.domain.records.nr_work_title_record import NRWorkTitleRecord
from validator.domain.records.nr_writer_name_record import NRWriterNameRecord
from validator.domain.records.performing_artist_record import PerformingArtistRecord
from validator.domain.records.publisher_control_record import PublisherControlRecord
from validator.domain.records.publisher_territory_record import PublisherTerritoryRecord
from validator.domain.records.recording_detail_record import RecordingDetailRecord
from validator.domain.records.registration_record import RegistrationRecord
from validator.domain.records.territory_record import TerritoryRecord
from validator.domain.records.transmission_header_record import TransmissionHeaderRecord
from validator.domain.records.transmission_trailer_record import TransmissionTrailerRecord
from validator.domain.records.work_additional_info_record import WorkAdditionalInfoRecord
from validator.domain.records.work_alternative_title_record import WorkAlternativeTitleRecord
from validator.domain.records.work_composite_record import WorkCompositeRecord
from validator.domain.records.work_excerpt_title import WorkExcerptTitle
from validator.domain.records.work_origin_record import WorkOriginRecord
from validator.domain.records.work_version_title import WorkVersionTitle
from validator.domain.records.writer_agent_record import WriterAgentRecord
from validator.domain.records.writer_control_record import WriterControlRecord
from validator.domain.records.writer_territory_record import WriterTerritoryRecord

__author__ = 'Borja'


class Document(object):
    def __init__(self, filename=None):
        self._name = filename
        self._last_group = None
        self._last_record_type = None
        self._last_transaction = None

        self._transmission_header = None
        self._transmission_trailer = None
        self._groups = {}
        self._group_types = {}

        self._transactions = {}
        self._records = {}
        self._errors = {}

        self._groups_number = 0
        self._transactions_number = 0
        self._records_number = 0

    def add_record(self, record=None):
        record_utf8 = record.encode('utf-8')
        record_type = record_utf8[0:3]
        self._records_number += 1

        if self._last_record_type == 'GRT' and record_type not in ['GRH', 'TRL']:
            raise FileRejectedError('Expected a group header or a transmission trailer to be after group trailer',
                                    record)

        if self._last_record_type == 'TRL':
            raise FileRejectedError('Transmission trailer expected to be the last record of the document', record)

        try:
            if record_type == 'HDR':
                self._add_transmission_header(record_utf8)
            elif record_type == 'TRL':
                self._add_transmission_trailer(record_utf8)
            elif record_type == 'GRH':
                self._add_group_header_record(record_utf8)
            elif record_type == 'GRT':
                self._add_group_trailer_record(record_utf8)
            elif record_type == 'AGR':
                self._add_agreement_record(record_utf8)
            elif record_type in ['NWR', 'REV']:
                self._add_registration_record(record_utf8)
            elif record_type == 'TER':
                self._add_territory_record(record_utf8)
            elif record_type == 'IPA':
                self._add_ipa_record(record_utf8)
            elif record_type == 'NPA':
                self._add_npa_record(record_utf8)
            elif record_type in ['SPU', 'OPU']:
                self._add_publisher_record(record_utf8)
            elif record_type == 'NPN':
                self._add_npn_record(record_utf8)
            elif record_type == 'SPT':
                self._add_publisher_territory_record(record_utf8)
            elif record_type in ['SWR', 'OWR']:
                self._add_writer_control_record(record_utf8)
            elif record_type == 'NWN':
                self._add_nwn_record(record_utf8)
            elif record_type == 'SWT':
                self._add_writer_territory_record(record_utf8)
            elif record_type == 'PWR':
                self._add_agent_record(record_utf8)
            elif record_type == 'ALT':
                self._add_alternative_title_record(record_utf8)
            elif record_type == 'NAT':
                self._add_nat_record(record_utf8)
            elif record_type == 'EWT':
                self._add_entire_title_record(record_utf8)
            elif record_type == 'VER':
                self._add_original_title_record(record_utf8)
            elif record_type == 'PER':
                self._add_performing_artist_record(record_utf8)
            elif record_type == 'NPR':
                self._add_npr_record(record_utf8)
            elif record_type == 'REC':
                self._add_recording_detail_record(record_utf8)
            elif record_type == 'ORN':
                self._add_work_origin_record(record_utf8)
            elif record_type == 'INS':
                self._add_instrumentation_summary_record(record_utf8)
            elif record_type == 'IND':
                self._add_instrumentation_detail_record(record_utf8)
            elif record_type == 'COM':
                self._add_component_record(record_utf8)
            elif record_type in ['NWT', 'NCT', 'NVT']:
                self._add_nr_title_record(record_utf8)
            elif record_type == 'NOW':
                self._add_now_record(record_utf8)
            elif record_type == 'ARI':
                self._add_additional_info_record(record_utf8)
            else:
                raise FileRejectedError('Not a valid transaction or detail record type', record, 'Record type')

            self._last_record_type = record_type
        except (RegexError, FieldValidationError, DocumentValidationError) as error:
            try:
                self._errors[int(record_utf8[11:19])] = (str('{} validation error: {} \n\t{}'.format(
                    record_type, str(error).replace("'", ""), record_utf8)).encode(encoding='utf-8', errors='replace'))
            except:
                print '----------------' + str(error)

    def _add_transmission_header(self, record):
        if self._transmission_header is not None:
            raise FileRejectedError('Expected only one transmission header')

        if self._last_record_type is not None or len(self._errors) != 0:
            raise FileRejectedError('Transmission header expected to be the first record of the document',
                                    record, None)

        self._transmission_header = TransmissionHeaderRecord(record)

    def _add_transmission_trailer(self, record):
        if self._transmission_trailer is not None:
            raise FileRejectedError('Expected only one transmission trailer')

        self._transmission_trailer = TransmissionTrailerRecord(record)
        if self._transmission_trailer.attr_dict['Group count'] != self._groups_number:
            raise FileRejectedError('Number of groups does not correspond with the processed ones {}'.format(
                self._groups_number), self._transmission_trailer, 'Group count')
        elif self._transmission_trailer.attr_dict['Transaction count'] != self._transactions_number:
            raise FileRejectedError('Number of transactions does not correspond with the processed ones {}'.format(
                self._transactions_number), self._transmission_trailer, 'Transaction count')
        elif self._transmission_trailer.attr_dict['Records count'] != self._records_number:
            raise FileRejectedError('Number of records does not correspond with the processed ones {}'.format(
                self._records_number), self._transmission_trailer, 'Transaction count')

    def _add_group_header_record(self, record):
        self._groups_number += 1

        group = GroupHeaderRecord(record)
        if self._last_record_type == 'HDR' and self._records_number != 2:
            raise FileRejectedError('Group header expected to be the second record of the document', group)
        elif self._last_record_type != 'GRT' and self._records_number != 2:
            raise FileRejectedError('Subsequents group header expected to be preceded by group trailers'.group)

        if self._last_group is not None:
            raise FileRejectedError('Group header encountered within another group', group)

        if group.attr_dict['Transaction type'] in self._group_types.keys():
            raise GroupRejectedError(group, 'Multiple groups for same transaction type', group, 'Transaction type')
        elif group.attr_dict['Group ID'] in self._groups.keys():
            raise GroupRejectedError(group, 'Multiple groups with same ID', group, 'Group ID')
        elif len(self._groups) + 1 != group.attr_dict['Group ID']:
            raise GroupRejectedError('Group ID must start in one and be incremented by one', group, 'Group ID')
        else:
            self._last_group = group

    def _add_group_trailer_record(self, record):
        trailer = GroupTrailerRecord(record)
        if trailer.attr_dict['Group ID'] != self._last_group.attr_dict['Group ID']:
            raise GroupRejectedError(self._last_group, 'Group trailer does not match the previous header ID',
                                     trailer, 'Group ID')
        elif trailer.attr_dict['Transaction count'] != len(self._last_group.transactions()):
            raise GroupRejectedError(self._last_group,
                                     'Transaction count does not match the number of transactions: {}'.format(
                                         len(self._last_group.transactions())),
                                     trailer)
        elif trailer.attr_dict['Record count'] != self._last_group.get_records_count():
            raise GroupRejectedError(self._last_group,
                                     'Record count does not match the number of records: {}'.format(
                                         self._last_group.get_records_count()),
                                     trailer)
        else:
            self._last_group.add_trailer(trailer)
            self._groups[trailer.attr_dict['Group ID']] = self._last_group
            self._group_types = self._last_group.attr_dict['Transaction type']
            self._last_group = None

    def _add_transaction(self, transaction):
        if self._last_transaction is not None:
            self._last_transaction.validate_transaction()
            self.transactions[
                self._last_transaction.attr_dict['Record prefix'].transaction_number] = self._last_transaction
            self._last_transaction = None

        if transaction.attr_dict['Record prefix'].record_type != self._last_group.attr_dict['Transaction type']:
            raise GroupRejectedError(self._last_group, 'Transaction record found outside its container group',
                                     transaction, 'Record prefix')

        if transaction.attr_dict['Record prefix'].record_number != 0:
            raise FileRejectedError('Record sequence must be zero within a transaction header',
                                    transaction, 'Record sequence')

        if len(self._transactions) == 0 and transaction.attr_dict['Record prefix'].transaction_number != 0:
            raise FileRejectedError('The first transaction within a file must have transaction sequence equals to zero',
                                    transaction, 'Transaction sequence')

        if len(self._transactions) != transaction.attr_dict['Record prefix'].transaction_number:
            raise TransactionRejectedError('Transaction sequence must be incremented by one',
                                           transaction, 'Transaction sequence')

        self._last_transaction = transaction

    def _add_agreement_record(self, record):
        self._transactions_number += 1

        transaction = AgreementRecord(record)
        self._add_transaction(transaction)

    def _add_registration_record(self, record):
        self._transactions_number += 1

        transaction = RegistrationRecord(record)
        self._add_transaction(transaction)

    def _add_record_to_transaction(self, record):
        if self._last_record_type == 'GRT':
            raise FileRejectedError('Expected a transaction to follow a group header record', record)

        if record.attr_dict['Record prefix'].transaction_number not in self._transactions.keys():
            raise DocumentValidationError('Record transaction number {} is not found'.format(
                record.attr_dict['Record prefix'].transaction_number))

        transaction = self._transactions[record.attr_dict['Record prefix'].transaction_number]
        if record.attr_dict['Record prefix'].record_number not in self._records.keys() \
                and record.attr_dict['Record prefix'].record_number not in self._errors.keys():
            transaction.add_record(record)
            self._records[record.attr_dict['Record prefix'].record_number] = record
        else:
            try:
                raise DocumentValidationError("Two records have the same number: \n {} \n {}".format(
                    self._records[record.attr_dict['Record prefix'].record_number], record))
            except KeyError:
                raise DocumentValidationError("Two records have the same number: \n {} \n {}".format(
                    self._errors[record.attr_dict['Record prefix'].record_number], record))

    def _add_territory_record(self, record):
        territory = TerritoryRecord(record)
        if self._last_transaction_type != 'AGR':
            raise DocumentValidationError('TER record expected within AGR transactions')
        if self._last_record_type not in ['AGR', 'TER']:
            raise DocumentValidationError('TER records expected after AGR or TER, found {}'.format(
                self._last_record_type))

        self._add_record_to_transaction(territory)

    def _add_ipa_record(self, record):
        ipa = InterestedPartyRecord(record)
        if self._last_transaction_type != 'AGR':
            raise DocumentValidationError('IPA record expected within AGR transactions')
        if self._last_record_type not in ['TER', 'IPA']:
            raise DocumentValidationError('IPA records expected after TER or IPA, found {}'.format(
                self._last_record_type))

        self._add_record_to_transaction(ipa)

    def _add_npa_record(self, record):
        npa = NRAgreementPartyNameRecord(record)
        if self._last_transaction_type != 'AGR':
            raise DocumentValidationError('NPA record expected within AGR transactions')
        if self._last_record_type != 'IPA' \
                and self._get_last_record(npa).attr_dict['Interested party ID'] != npa.attr_dict['Interested party ID']:
            raise DocumentValidationError('NPA must follow an IPA record and share the Interested party ID')

        self._add_record_to_transaction(npa)

    def _add_publisher_record(self, record):
        publisher = PublisherControlRecord(record)

        self._add_record_to_transaction(publisher)

    def _add_npn_record(self, record):
        npn = NRPublisherNameRecord(record)
        if self._last_record_type != 'SPU' \
                and self._get_last_record(npn).attr_dict['Interested party ID'] != npn.attr_dict['Interested party ID']:
            raise DocumentValidationError('NPN must follow a SPU record and share the Interested party ID')

        self._add_record_to_transaction(npn)

    def _add_publisher_territory_record(self, record):
        territory = PublisherTerritoryRecord(record)
        if self._last_record_type not in ['SPU', 'SPT']:
            raise DocumentValidationError('SPT must follow a SPU or SPT record')

        count = 1
        publisher = None
        while territory.attr_dict['Record prefix'].record_number - count in self._records.keys() or \
                                territory.attr_dict['Record prefix'].record_number - count in self._errors.keys():
            if territory.attr_dict['Record prefix'].record_number - count not in self._errors.keys():
                publisher = self._records.get(territory.attr_dict['Record prefix'].record_number - count, None)

                if publisher is not None and publisher.attr_dict['Record prefix'].record_type == 'SPU':
                    break
                else:
                    publisher = None
                    count += 1
            else:
                raise DocumentValidationError('Previous record: {} was incorrect'.format(
                    self._errors[territory.attr_dict['Record prefix'].record_number - count]))

        if publisher is None:
            raise DocumentValidationError('Expected publisher for SPT record')

        if publisher is not None \
                and publisher.attr_dict['Interested party ID'] != territory.attr_dict['Interested party ID']:
            raise DocumentValidationError('Preceding SPU record to SPT must share interested party ID')

        self._add_record_to_transaction(territory)

    def _add_writer_control_record(self, record):
        writer = WriterControlRecord(record)
        self._add_record_to_transaction(writer)

    def _add_nwn_record(self, record):
        nwn = NRWriterNameRecord(record)
        if self._last_record_type != 'SWR' \
                and self._get_last_record(nwn).attr_dict['Interested party ID'] != nwn.attr_dict['Interested party ID']:
            raise DocumentValidationError('NWN must follow a SWR record and share the Interested party ID')

        self._add_record_to_transaction(nwn)

    def _add_writer_territory_record(self, record):
        territory = WriterTerritoryRecord(record)
        if self._last_record_type not in ['SWR', 'SWT']:
            raise DocumentValidationError('SWT must follow a SWR or SWT record')

        count = 1
        writer = None
        while territory.attr_dict['Record prefix'].record_number - count in self._records.keys() or \
                                territory.attr_dict['Record prefix'].record_number - count in self._errors.keys():
            if territory.attr_dict['Record prefix'].record_number - count not in self._errors.keys():
                writer = self._records[territory.attr_dict['Record prefix'].record_number - count]
                if writer.attr_dict['Record prefix'].record_type == 'SWR':
                    break
                else:
                    writer = None
                    count += 1
            else:
                raise DocumentValidationError("Previous record: {} was incorrect, so this can't be evaluated".format(
                    self._errors[territory.attr_dict['Record prefix'].record_number - count]))

        if writer is None:
            raise DocumentValidationError('Expected writer for SWT record')

        if writer.attr_dict['Interested party ID'] != territory.attr_dict['Interested party ID']:
            raise DocumentValidationError('Preceding SWR record to SWT must share interested party ID')

        self._add_record_to_transaction(territory)

    def _add_agent_record(self, record):
        agent = WriterAgentRecord(record)
        if self._last_record_type not in ['SWR', 'SWT', 'PWR']:
            raise DocumentValidationError('PWR must follow a SWR or SWT or PWR record')
        if self._last_transaction_type != 'NWR':
            raise DocumentValidationError('PWR must be within NWR transaction')

        writer = None
        publisher = None
        count = 1
        while agent.attr_dict['Record prefix'].record_number - count in self._records.keys() or \
                                agent.attr_dict['Record prefix'].record_number - count in self._errors.keys():
            if agent.attr_dict['Record prefix'].record_number - count not in self._errors.keys():
                ipa = self._records[agent.attr_dict['Record prefix'].record_number - count]
                if ipa.attr_dict['Record prefix'].record_type == 'SWR':
                    writer = ipa
                elif ipa.attr_dict['Record prefix'].record_type == 'SPU':
                    publisher = ipa

                count += 1
                if writer is not None and publisher is not None:
                    break
            else:
                raise DocumentValidationError("Previous record: {} was incorrect, so this can't be evaluated".format(
                    self._errors[agent.attr_dict['Record prefix'].record_number - count]))

        if publisher is None or writer is None:
            raise DocumentValidationError('Writer and publisher must be known for a PWT record')

        if publisher is not None \
                and publisher.attr_dict['Interested party ID'] != agent.attr_dict['Publisher IP ID']:
            raise DocumentValidationError('PWR publisher ID must match preceding SPU record IP ID')

        if writer is not None \
                and writer.attr_dict['Interested party ID'] != agent.attr_dict['Writer IP ID']:
            raise DocumentValidationError('PWR writer ID must match preceding SWR record IP ID')

        self._add_record_to_transaction(agent)

    def _add_alternative_title_record(self, record):
        title = WorkAlternativeTitleRecord(record)
        self._add_record_to_transaction(title)

    def _add_nat_record(self, record):
        title = NRWorkTitleRecord(record)
        self._add_record_to_transaction(title)

    def _add_entire_title_record(self, record):
        title = WorkExcerptTitle(record)
        self._add_record_to_transaction(title)

    def _add_original_title_record(self, record):
        title = WorkVersionTitle(record)
        self._add_record_to_transaction(title)

    def _add_performing_artist_record(self, record):
        artist = PerformingArtistRecord(record)
        self._add_record_to_transaction(artist)

    def _add_npr_record(self, record):
        performance = NRPerformanceDataRecord(record)
        self._add_record_to_transaction(performance)

    def _add_recording_detail_record(self, record):
        detail = RecordingDetailRecord(record)
        self._add_record_to_transaction(detail)

    def _add_work_origin_record(self, record):
        work = WorkOriginRecord(record)
        self._add_record_to_transaction(work)

    def _add_instrumentation_summary_record(self, record):
        summary = InstrumentationSummaryRecord(record)
        self._add_record_to_transaction(summary)

    def _add_instrumentation_detail_record(self, record):
        detail = InstrumentationDetailRecord(record)
        if self._last_record_type not in ['INS', 'IND']:
            raise DocumentValidationError('IND record type must follow an INS or IND record')

        self._add_record_to_transaction(detail)

    def _add_component_record(self, record):
        component = WorkCompositeRecord(record)
        self._add_record_to_transaction(component)

    def _add_nr_title_record(self, record):
        title = NRSpecialTitleRecord(record)
        record_type = record[0:3]
        if record_type == 'NET' and self._last_record_type != 'EWT':
            raise DocumentValidationError('NET record type must follow an EWT record')
        elif record_type == 'NCT' and self._last_record_type != 'COM':
            raise DocumentValidationError('NCT record type must follow a COM record')
        if record_type == 'NVT' and self._last_record_type != 'VET':
            raise DocumentValidationError('NVT record type must follow a VER record')

        self._add_record_to_transaction(title)

    def _add_now_record(self, record):
        writer = NROtherWriterRecord(record)
        if self._last_record_type not in ['EWT', 'VER', 'COM', 'NET', 'NCT', 'NVT']:
            raise DocumentValidationError('NOW record type must follow an {} record'.format(
                'or'.join(['EWT', 'VER', 'COM', 'NET', 'NCT', 'NVT'])))

        self._add_record_to_transaction(writer)

    def _add_additional_info_record(self, record):
        info = WorkAdditionalInfoRecord(record)

        self._add_record_to_transaction(info)

    def _get_last_record(self, record):
        return self._records[record.attr_dict['Record prefix'].record_number - 1]

    def validate(self):
        if self._transmission_header is None:
            raise FileRejectedError('Expected to have at least one transmission header')
        if self._transmission_trailer is None:
            raise FileRejectedError('expected to have at least one transmission trailer')

    @property
    def errors(self):
        return self._errors

    @property
    def transactions(self):
        return self._transactions