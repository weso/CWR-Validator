from validator.domain.exceptions.file_rejected_error import FileRejectedError
from validator.domain.exceptions.group_rejected_error import GroupRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
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

import logging


class Document(object):
    NO_DETAIL_RECORDS = ['HDR', 'TRL', 'GRH', 'GRT', 'AGR', 'NWR', 'REV']

    def __init__(self, filename=None):
        logging.basicConfig(filename='validator.log', filemode="w", level=logging.DEBUG)

        self._name = filename
        self._last_group = None
        self._last_record_type = None
        self._last_transaction = None
        self._last_record = None

        self._transmission_header = None
        self._transmission_trailer = None
        self._groups = {}
        self._group_types = {}

        self._transactions = {}
        self._records = {}
        self._transaction_errors = {}
        self._record_errors = {}

        self._groups_number = 0
        self._transactions_number = 0
        self._records_number = 0

        self._rejected = False
        self._rejected_reason = None

    def add_record(self, record=None):
        record_utf8 = record.encode('utf-8')
        record_type = record_utf8[0:3]
        record_number = None
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
            else:
                record_number = int(record_utf8[3:11])
                self._last_group.inc_transactions()
                if record_type == 'AGR':
                    self._add_agreement_record(record_utf8)
                elif record_type in ['NWR', 'REV']:
                    self._add_registration_record(record_utf8)
                else:
                    self._last_group.inc_records()
                    if record_type == 'TER':
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

                    self._records[record_number] = self._last_record

            self._last_record.validate_record()
            self._last_record_type = record_type

        except RecordRejectedError as error:
            self._reject_record(record_number, record_type, error)
        except TransactionRejectedError as error:
            self._reject_transaction(record_number, record_type, error)
        except GroupRejectedError:
            self._reject_group(record_type)

        logging.debug(record)
        logging.debug("Transactions {},  Records {}".format(len(self._transactions), len(self._records)))

    def _reject_group(self, record_type):
        self._last_group._rejected = True
        self._last_record_type = record_type

    def _reject_transaction(self, record_number, record_type, error):
        self._reject_record(record_number, record_type, error)
        self._last_transaction._rejected = True
        self.transactions[
            self._last_transaction.attr_dict['Record prefix'].transaction_number] = self._last_transaction
        self._transaction_errors[self._last_transaction.attr_dict['Record prefix'].transaction_number] = error

    def _reject_record(self, record_number, record_type, error):
        self._last_record._rejected = True
        self._last_record_type = record_type

        if record_type not in self.NO_DETAIL_RECORDS:
            logging.warning("{}".format(error))
            self._records[record_number] = self._last_record
            self._record_errors[record_number] = error

    def _add_transmission_header(self, record):
        if self._transmission_header is not None:
            raise FileRejectedError('Expected only one transmission header')

        if self._last_record_type is not None or len(self._record_errors) != 0:
            raise FileRejectedError('Transmission header expected to be the first record of the document',
                                    record, None)

        self._transmission_header = TransmissionHeaderRecord(record)
        self._last_record = self._transmission_header

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
        elif self._transmission_trailer.attr_dict['Record count'] != self._records_number:
            raise FileRejectedError('Number of records does not correspond with the processed ones {}'.format(
                self._records_number), self._transmission_trailer, 'Transaction count')

        self._last_record = self._transmission_trailer

    def _add_group_header_record(self, record):
        if self._last_group is not None:
            self._groups[self._last_group.attr_dict['Group ID']] = self._last_group
            self._group_types[self._last_group.attr_dict['Transaction type']] = self._last_group

        self._groups_number += 1
        group = GroupHeaderRecord(record)

        if self._last_record_type == 'HDR' and self._records_number != 2:
            raise FileRejectedError('Group header expected to be the second record of the document', group)
        elif self._last_record_type != 'GRT' and self._records_number > 2:
            raise FileRejectedError('Subsequents group header expected to be preceded by group trailers', group)

        if self._last_group is not None and self._last_group.trailer is None:
            raise FileRejectedError('Group header encountered within another group', group)

        self._last_group = group
        self._last_record = group
        if group.attr_dict['Transaction type'] in self._group_types.keys():
            raise GroupRejectedError(group, 'Multiple groups for same transaction type', group, 'Transaction type')
        elif group.attr_dict['Group ID'] in self._groups.keys():
            raise GroupRejectedError(group, 'Multiple groups with same ID', group, 'Group ID')
        elif len(self._groups) + 1 != group.attr_dict['Group ID']:
            raise GroupRejectedError('Group ID must start in one and be incremented by one', group, 'Group ID')

    def _add_group_trailer_record(self, record):
        trailer = GroupTrailerRecord(record)
        self._last_record = trailer

        self._last_group.add_trailer(trailer)

        if trailer.attr_dict['Group ID'] != self._last_group.attr_dict['Group ID']:
            raise GroupRejectedError(self._last_group, 'Group trailer does not match the previous header ID',
                                     trailer, 'Group ID')
        elif trailer.attr_dict['Transaction count'] != len(self._last_group.transactions):
            raise GroupRejectedError(self._last_group,
                                     'Transaction count does not match the number of transactions: {}'.format(
                                         len(self._last_group.transactions)),
                                     trailer)
        elif trailer.attr_dict['Record count'] != self._last_group.records_number:
            raise GroupRejectedError(self._last_group,
                                     'Record count does not match the number of records: {}'.format(
                                         self._last_group.records_number),
                                     trailer)

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

        self._last_record = transaction
        self._last_transaction = transaction
        self._last_group.add_transaction(transaction)

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

        if record.attr_dict['Record prefix'].transaction_number != self._last_transaction.attr_dict[
                'Record prefix'].transaction_number:
            raise RecordRejectedError('Record transaction number is not found', record, 'Transaction number')

        if record.attr_dict['Record prefix'].record_number not in self._records.keys() \
                and record.attr_dict['Record prefix'].record_number not in self._record_errors.keys():
            self._last_transaction.add_record(record)
            self._records[record.attr_dict['Record prefix'].record_number] = record
        else:
            raise RecordRejectedError('Duplicated value', record, 'Record number')

    def _add_territory_record(self, record):
        self._last_record = TerritoryRecord(record, self._last_transaction)
        if self._last_record_type not in ['AGR', 'TER']:
            raise TransactionRejectedError(self._last_transaction, 'TER records expected after AGR or TER',
                                           self._last_record)

        self._add_record_to_transaction(self._last_record)

    def _add_ipa_record(self, record):
        self._last_record = InterestedPartyRecord(record, self._last_transaction)
        if self._last_record_type not in ['TER', 'IPA']:
            raise TransactionRejectedError(self._last_transaction, 'IPA records expected after TER or IPA',
                                           self._last_record)

        self._add_record_to_transaction(self._last_record)

    def _add_npa_record(self, record):
        self._last_record = NRAgreementPartyNameRecord(record, self._last_transaction)
        if self._last_record_type != 'IPA' \
                and self._get_last_record(self._last_record).attr_dict['Interested party ID'] != \
                self._last_record.attr_dict['Interested party ID']:
            raise RecordRejectedError('NPA must follow an IPA record and share the Interested party ID',
                                      self._last_record)

        self._add_record_to_transaction(self._last_record)

    def _add_publisher_record(self, record):
        self._last_record = PublisherControlRecord(record, self._last_transaction)

        self._add_record_to_transaction(self._last_record)

    def _add_npn_record(self, record):
        self._last_record = NRPublisherNameRecord(record, self._last_transaction)
        if self._last_record_type != 'SPU' \
                and self._get_last_record(self._last_record).attr_dict['Interested party ID'] != \
                self._last_record.attr_dict['Interested party ID']:
            raise RecordRejectedError('NPN must follow a SPU record and share the Interested party ID', record)

        self._add_record_to_transaction(self._last_record)

    def _add_publisher_territory_record(self, record):
        self._last_record = PublisherTerritoryRecord(record, self._last_transaction)
        if self._last_record_type not in ['SPU', 'SPT']:
            raise TransactionRejectedError(self._last_transaction, 'SPT must follow a SPU or SPT record',
                                           self._last_record)

        count = 1
        publisher = None
        while self._last_record.attr_dict['Record prefix'].record_number - count in self._records.keys() or \
                self._last_record.attr_dict['Record prefix'].record_number - count in self._record_errors.keys():
            if self._last_record.attr_dict['Record prefix'].record_number - count not in self._record_errors.keys():
                publisher = self._records.get(self._last_record.attr_dict['Record prefix'].record_number - count, None)

                if publisher is not None and publisher.attr_dict['Record prefix'].record_type == 'SPU':
                    break
                else:
                    publisher = None
                    count += 1
            else:
                raise RecordRejectedError('Previous record was incorrect', self._last_record)

        if publisher is None:
            raise TransactionRejectedError(self._last_transaction, 'Expected publisher for SPT record')

        if publisher is not None \
                and publisher.attr_dict['Interested party ID'] != self._last_record.attr_dict['Interested party ID']:
            raise TransactionRejectedError(self._last_transaction,
                                           'Preceding SPU record to SPT must share interested party ID')

        self._add_record_to_transaction(self._last_record)

    def _add_writer_control_record(self, record):
        self._last_record = WriterControlRecord(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_nwn_record(self, record):
        self._last_record = NRWriterNameRecord(record, self._last_transaction)
        if self._last_record_type != 'SWR' \
                and self._get_last_record(self._last_record).attr_dict['Interested party ID'] != \
                self._last_record.attr_dict['Interested party ID']:
            raise RecordRejectedError('NWN must follow a SWR record and share the Interested party ID',
                                      self._last_record, 'Interested party ID')

        self._add_record_to_transaction(self._last_record)

    def _add_writer_territory_record(self, record):
        self._last_record = WriterTerritoryRecord(record, self._last_transaction)
        if self._last_record_type not in ['SWR', 'SWT']:
            raise TransactionRejectedError(self._last_transaction, 'SWT must follow a SWR or SWT record')

        count = 1
        writer = None
        while self._last_record.attr_dict['Record prefix'].record_number - count in self._records.keys() or \
                self._last_record.attr_dict['Record prefix'].record_number - count in self._record_errors.keys():
            if self._last_record.attr_dict['Record prefix'].record_number - count not in self._record_errors.keys():
                writer = self._records[self._last_record.attr_dict['Record prefix'].record_number - count]
                if writer.attr_dict['Record prefix'].record_type == 'SWR':
                    break
                else:
                    writer = None
                    count += 1
            else:
                raise RecordRejectedError('Previous record was incorrect', self._last_record)

        if writer is None:
            raise TransactionRejectedError(self._last_transaction, 'Expected writer for SWT record', self._last_record)

        if writer.attr_dict['Interested party ID'] != self._last_record.attr_dict['Interested party ID']:
            raise TransactionRejectedError(self._last_transaction, 'Preceding SWR must share interested party ID',
                                           self._last_record, 'Interested party ID')

        self._add_record_to_transaction(self._last_record)

    def _add_agent_record(self, record):
        self._last_record = WriterAgentRecord(record, self._last_transaction)
        if self._last_record_type not in ['SWR', 'SWT', 'PWR']:
            raise RecordRejectedError('PWR must follow a SWR or SWT or PWR record', self._last_record)

        writer = None
        publisher = None
        count = 1
        while self._last_record.attr_dict['Record prefix'].record_number - count in self._records.keys() or \
                self._last_record.attr_dict['Record prefix'].record_number - count in self._record_errors.keys():
            if self._last_record.attr_dict['Record prefix'].record_number - count not in self._record_errors.keys():
                ipa = self._records[self._last_record.attr_dict['Record prefix'].record_number - count]
                if ipa.attr_dict['Record prefix'].record_type == 'SWR':
                    writer = ipa
                elif ipa.attr_dict['Record prefix'].record_type == 'SPU':
                    publisher = ipa

                count += 1
                if writer is not None and publisher is not None:
                    break
            else:
                raise RecordRejectedError('Previous record was incorrect', self._last_record)

        if publisher is None or writer is None:
            raise RecordRejectedError('Writer and publisher must be known for a PWT record', self._last_record)

        if publisher is not None \
                and publisher.attr_dict['Interested party ID'] != self._last_record.attr_dict['Publisher IP ID']:
            raise RecordRejectedError('PWR publisher ID must match preceding SPU record IP ID', self._last_record,
                                      'Interested party ID')

        if writer is not None \
                and writer.attr_dict['Interested party ID'] != self._last_record.attr_dict['Writer IP ID']:
            raise RecordRejectedError('PWR publisher ID must match preceding SWR record IP ID', self._last_record,
                                      'Interested party ID')

        self._add_record_to_transaction(self._last_record)

    def _add_alternative_title_record(self, record):
        self._last_record = WorkAlternativeTitleRecord(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_nat_record(self, record):
        self._last_record = NRWorkTitleRecord(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_entire_title_record(self, record):
        self._last_record = WorkExcerptTitle(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_original_title_record(self, record):
        self._last_record = WorkVersionTitle(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_performing_artist_record(self, record):
        self._last_record = PerformingArtistRecord(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_npr_record(self, record):
        self._last_record = NRPerformanceDataRecord(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_recording_detail_record(self, record):
        self._last_record = RecordingDetailRecord(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_work_origin_record(self, record):
        self._last_record = WorkOriginRecord(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_instrumentation_summary_record(self, record):
        self._last_record = InstrumentationSummaryRecord(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_instrumentation_detail_record(self, record):
        self._last_record = InstrumentationDetailRecord(record, self._last_transaction)
        if self._last_record_type not in ['INS', 'IND']:
            raise RecordRejectedError('IND record type must follow an INS or IND record', record)

        self._add_record_to_transaction(self._last_record)

    def _add_component_record(self, record):
        self._last_record = WorkCompositeRecord(record, self._last_transaction)
        self._add_record_to_transaction(self._last_record)

    def _add_nr_title_record(self, record):
        self._last_record = NRSpecialTitleRecord(record, self._last_transaction)
        record_type = record[0:3]
        if record_type == 'NET' and self._last_record_type != 'EWT':
            raise RecordRejectedError('NET record type must follow an EWT record', record)
        elif record_type == 'NCT' and self._last_record_type != 'COM':
            raise RecordRejectedError('NCT record type must follow a COM record', record)
        if record_type == 'NVT' and self._last_record_type != 'VET':
            raise RecordRejectedError('NVT record type must follow a VER record', record)

        self._add_record_to_transaction(self._last_record)

    def _add_now_record(self, record):
        self._last_record = NROtherWriterRecord(record, self._last_transaction)
        if self._last_record_type not in ['EWT', 'VER', 'COM', 'NET', 'NCT', 'NVT']:
            raise RecordRejectedError('NOW record type must follow an {} record'.format(
                'or'.join(['EWT', 'VER', 'COM', 'NET', 'NCT', 'NVT'])), record)

        self._add_record_to_transaction(self._last_record)

    def _add_additional_info_record(self, record):
        self._last_record = WorkAdditionalInfoRecord(record, self._last_transaction)

        self._add_record_to_transaction(self._last_record)

    def _get_last_record(self, record):
        return self._records[record.attr_dict['Record prefix'].record_number - 1]

    def validate(self):
        if self._transmission_header is None:
            raise FileRejectedError('Expected to have at least one transmission header')
        if self._transmission_trailer is None:
            raise FileRejectedError('expected to have at least one transmission trailer')

    def reject(self, error):
        self._rejected = True
        self._rejected_reason = error

    @property
    def errors(self):
        return self._record_errors

    @property
    def transactions(self):
        return self._transactions