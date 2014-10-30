from datetime import datetime

from utils import functions
from utils.value_tables import AGREEMENT_TYPE_VALUES, TRANSACTION_VALUES, TIS_CODES, SOCIETY_CODES, \
    WRITER_DESIGNATIONS, LANGUAGE_CODES, INTENDED_PURPOSES, SENDER_VALUES, INSTRUMENT_CODES, TITLE_TYPES, \
    PUBLISHER_TYPES, RECORDING_FORMAT, RECORDING_TECHNIQUE, MEDIA_TYPES, DISTRIBUTION_CATEGORY_TABLE, VERSION_TYPES, \
    MUSIC_ARRANGEMENT_TYPES, LYRIC_ADAPTATION, TEXT_MUSIC_TABLE, COMPOSITE_TYPE, EXCERPT_TYPE, WORK_TYPES, \
    RIGHT_TYPES, SUBJECT_CODES


__author__ = 'Borja'
import abc


class CWRField(object):
    def __init__(self, name, regular_expression, value=None):
        self._name = name.replace(' ', '_').lower()
        self._regular_expression = regular_expression
        self._value = value
        self._rejected = False

    @property
    def name(self):
        return self._name

    @property
    def rejected(self):
        return self._rejected

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def regular_expression(self):
        return self._regular_expression

    def reject(self, default_value=None):
        """
        When the field is rejected the value becomes its default value or none
        :return: None
        """
        self._rejected = True
        self._value = default_value

    def check(self, expected_values, optional=False, default_value=None):
        if optional and self._value is None:
            pass
        elif self._value not in expected_values or optional:
            self.reject(default_value)

        return self._rejected

    def format(self, format_type, default_value=None):
        try:
            if format_type == 'boolean':
                self.format_boolean_value()
            elif format_type == 'date':
                self.format_date_value()
            elif format_type == 'integer':
                self.format_integer_value()
            elif format_type == 'float':
                self.format_float_value(3)
            elif format_type == 'time':
                self.format_time_value()
        except (TypeError, ValueError):
            self.reject(default_value)

        return self._rejected

    def format_boolean_value(self):
        self._value = (self._value == 'Y')

    def format_date_value(self):
        if int(self._value) != 0:
            self._value = datetime.strptime(self._value, '%Y%m%d').date() if self._value else None
        else:
            self._value = None

    def format_integer_value(self):
        self._value = int(self._value) if self._value else None

    def format_float_value(self, integer_part_size):
        self.value = float(
            self._value[0:0 + integer_part_size] + '.' + self._value[0 + integer_part_size:len(self._value)]) \
            if self._value else None

    def format_time_value(self):
        if int(self._value) != 0:
            self._value = datetime.strptime(self._value, '%H%M%S').time() if self._value else None
        else:
            self._value = None

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return self._value


class CWRMessage(object):
    TYPES = functions.enum(FIELD='F', RECORD='R', TRANSACTION='T', GROUP='G', FILE='E')

    def __init__(self, msg_type, original_record, record_type, msg_level, msg_text):
        self._transaction_type = 'MSG'
        self._msg_type = msg_type
        self._original_record = original_record
        self._record_type = record_type
        self._msg_level = msg_level
        self._validation_number = self._generate_validation_number()
        self._msg_text = msg_text

    @staticmethod
    def _generate_validation_number():
        # TODO
        return "000"

    def __str__(self):
        return self._transaction_type + self._msg_type + self._original_record + self._record_type + self._msg_level + \
            self._validation_number + self._msg_text

    def __repr__(self):
        return self.__str__()


class CWRObject(object):
    def __init__(self, number, record, fields):
        self._number = number
        self._record = record
        self._rejected = False

        self.record_type = None
        self.transaction_number = None
        self.record_number = None
        self.raw_record_number = None

        for field in fields:
            if hasattr(self, field.name):
                setattr(self, field.name, field)

        self._last_record = self.record_type.value

        self._messages = []

        self.format_fields()

    @property
    def record(self):
        return self._record

    @property
    def number(self):
        return self._number

    @property
    def rejected(self):
        return self._rejected

    @property
    def messages(self):
        return self._messages

    def reject(self, msg_text, record=None, msg_type=CWRMessage.TYPES.RECORD, msg_level=CWRMessage.TYPES.RECORD):
        rejection_record = self if record is None else record
        rejection_number = rejection_record.raw_record_number if rejection_record.record_number is not None \
            else "00000000"
        message = CWRMessage(msg_type, rejection_number, rejection_record.record_type.value, msg_level, msg_text)
        self._messages.append(message)

        self._rejected = True

    def format_fields(self):
        if self.record_number is not None:
            self.raw_record_number = self.record_number.value
            self.record_number.format('integer')

        if self.transaction_number is not None:
            self.transaction_number.format('integer')

    @abc.abstractmethod
    def field_level_validation(self):
        pass

    @abc.abstractmethod
    def record_level_validation(self):
        pass

    @abc.abstractmethod
    def transaction_level_validation(self, transaction):
        pass

    @abc.abstractmethod
    def group_level_validation(self, group):
        pass

    @abc.abstractmethod
    def file_level_validation(self, document):
        pass

    def __str__(self):
        return str(self._record)

    def __repr__(self):
        return self.__str__()


class Agreement(CWRObject):
    def __init__(self, number, record, fields):
        self.records = []

        self._territories = []
        self._interested_parties = {}

        self.submitter_number = None
        self.international_standard_number = None
        self.type = None
        self.start_date = None
        self.end_date = None
        self.retention_end_date = None
        self.prior_royalty_status = None
        self.prior_royalty_status_date = None
        self.post_term_collection_status = None
        self.post_term_collection_end_date = None
        self.signature_date = None
        self.works_number = None
        self.sales_manufacture_clause = None
        self.shares_change = None
        self.advance_given = None
        self.society_assigned_number = None

        super(Agreement, self).__init__(number, record, fields)

    def add_territory(self, territory):
        if self.transaction_number.value != territory.transaction_number.value:
            territory.reject('Wrong transaction number')
        else:
            if self._last_record not in ['AGR', 'TER']:
                self.transaction_reject('Unexpected territory record')

            self._territories.append(territory)
            self._last_record = territory.record_type.value

    def add_interested_party(self, ipa):
        if self.transaction_number.value != ipa.transaction_number.value:
            ipa.reject('Wrong transaction number')
        else:
            if ipa.record_type.value == 'NPA':
                if self._last_record != 'IPA' or ipa.interested_party_id.value not in self._interested_parties.keys():
                    ipa.reject('Interested party id does not correspond to precious interested party')

                self._interested_parties[str(ipa.interested_party_id)].nr_name = ipa
            else:
                if self._last_record not in ['IPA', 'NPA', 'TER']:
                    self.transaction_reject('Unexpected interested party record')

                self._interested_parties[str(ipa.id)] = ipa
            self._last_record = ipa.record_type.value

    def extract_records(self):
        records = []

        for ipa in self._interested_parties.values():
            records.append(ipa)
            if ipa.nr_name is not None:
                records.append(ipa.nr_name)

        records.extend(self._territories)

        self.records = records

        return records

    def format_fields(self):
        super(Agreement, self).format_fields()

        self.start_date.format('date')
        self.end_date.format('date')
        self.retention_end_date.format('date')
        self.prior_royalty_status_date.format('date')
        self.post_term_collection_end_date.format('date')
        self.signature_date.format('date')
        self.works_number.format('integer')

    def field_level_validation(self):
        for territory in self._territories:
            territory.field_level_validation()

        for ipa in self._interested_parties.values():
            ipa.field_level_validation()

        self.shares_change.check(['Y', 'N'], 'N')
        self.advance_given.check(['Y', 'N'], 'N')

    def record_level_validation(self):
        for territory in self._territories:
            territory.record_level_validation()

        for ipa in self._interested_parties.values():
            ipa.record_level_validation()

    def transaction_level_validation(self, transaction):
        for territory in self._territories:
            territory.transaction_level_validation(self)

        for ipa in self._interested_parties.values():
            ipa.transaction_level_validation(self)

        if len(self._territories) == 0:
            self.transaction_reject('Expected at least one territory record')

        if len(self._interested_parties) < 2 and not any(
                str(ipa.agreement_role_code.value) == 'AC' for ipa in self._interested_parties.values()) and not any(
                str(ipa.agreement_role_code.value) == 'AS' for ipa in self._interested_parties.values()):
            self.transaction_reject('Expected two interested parties, one as assignor and one as acquirer')

        if sum(ipa.pr_share.value for ipa in self._interested_parties.values()) != 100:
            self.transaction_reject('The total of PR Share within interested parties must be 100')
        if sum(ipa.mr_share.value for ipa in self._interested_parties.values()) != 100:
            self.transaction_reject('The total of MR Share within interested parties must be 100')
        if sum(ipa.sr_share.value for ipa in self._interested_parties.values()) != 100:
            self.transaction_reject('The total of SR Share within interested parties must be 100')

        if self.type.check(AGREEMENT_TYPE_VALUES):
            self.transaction_reject('Not a valid agreement type')
        if self.start_date.rejected:
            self.transaction_reject('Agreement start date not a valid date')
        if self.end_date.rejected:
            self.transaction_reject('End date not a valid date')
        if not self.retention_end_date.rejected and self.retention_end_date.value < self.end_date.value:
            self.transaction_reject('Retention end date must be equal or later to end date')

        if self.prior_royalty_status_date.rejected:
            self.transaction_reject('Status date not a valid date')
        if self.prior_royalty_status.value == 'D' and self.prior_royalty_status_date.value is None:
            self.transaction_reject('Expected prior royalty status date')
        elif self.prior_royalty_status_date.value >= self.start_date.value:
            self.transaction_reject('Prior royalty status must be earlier than start date')
        if self.prior_royalty_status.value in ['N', 'A'] and self.prior_royalty_status_date.value is not None:
            self.transaction_reject('Not expected prior royalty status date')

        if self.post_term_collection_end_date.rejected:
            self.transaction_reject('Post term collection end date not a valid date')
        if self.post_term_collection_end_date.value is not None and self.end_date.value is not None \
                and self.post_term_collection_end_date.value <= self.end_date.value:
            self.transaction_reject('Post term collection end date must be after end date')
        elif self.post_term_collection_end_date.value is not None and \
                self.post_term_collection_end_date.value <= self.start_date.value:
            self.transaction_reject('Post term collection end date must be after start date')
        if self.post_term_collection_status.value == 'D' and self.post_term_collection_end_date.value is None:
            self.transaction_reject('Expected post term collection end date')
        elif self.post_term_collection_status.value in ['N', 'O'] and \
                self.post_term_collection_end_date.value is not None:
            self.transaction_reject('Not expected post term end date')

        if self.type.value in ['OS', 'PS'] and self.sales_manufacture_clause.value is None:
            self.transaction_reject('Expected sales manufacture clause')

        if self.works_number.rejected or self.works_number.value <= 0:
            self.transaction_reject('Number of works must be greater than 0')

    def group_level_validation(self, group):
        for territory in self._territories:
            territory.group_level_validation(group)

        for ipa in self._interested_parties.values():
            ipa.group_level_validation(group)

    def file_level_validation(self, document):
        for territory in self._territories:
            territory.file_level_validation(document)

        for ipa in self._interested_parties.values():
            ipa.file_level_validation(document)

    def transaction_reject(self, msg_text, record=None):
        rejection_record = self if record is None else record

        super(Agreement, self).reject(msg_text, rejection_record, CWRMessage.TYPES.TRANSACTION,
                                      CWRMessage.TYPES.TRANSACTION)


class Group(CWRObject):
    def __init__(self, number, record, fields):
        self._transactions = []
        self._trailer = None

        self.transaction_type = None
        self.id = None
        self.transaction_type_version_number = None
        self.batch_request = None
        self.submission_distribution_type = None

        super(Group, self).__init__(number, record, fields)

    @property
    def transactions(self):
        return self._transactions

    def add_trailer(self, group_trailer):
        if self._trailer is None:
            if self.id.value == group_trailer.group_id.value:
                self._trailer = group_trailer
        else:
            self.group_reject('Group trailer does not match with the group id')

    def add_transaction(self, transaction):
        self._transactions.append(transaction)

    def format_fields(self):
        super(Group, self).format_fields()

        self.id.format('integer')
        self.batch_request.format('integer')

    def field_level_validation(self):
        for transaction in self._transactions:
            transaction.field_level_validation()

        self._trailer.field_level_validation()

    def record_level_validation(self):
        for transaction in self._transactions:
            transaction.record_level_validation()

        self._trailer.record_level_validation()

    def transaction_level_validation(self, transaction):
        for transaction in self._transactions:
            transaction.transaction_level_validation(transaction)

        self._trailer.transaction_level_validation(transaction)

    def group_level_validation(self, group):
        for transaction in self._transactions:
            transaction.group_level_validation(self)

        self._trailer.group_level_validation(self)

        if self.transaction_type.check(TRANSACTION_VALUES):
            self.group_reject('Transaction type is not valid')

    def file_level_validation(self, document):
        for transaction in self._transactions:
            transaction.file_level_validation(document)

        self._trailer.file_level_validation(document)

    def group_reject(self, msg_text, record=None):
        rejection_record = self if record is None else record
        super(Group, self).reject(msg_text, rejection_record, CWRMessage.TYPES.GROUP, CWRMessage.TYPES.GROUP)


class GroupTrailer(CWRObject):
    def __init__(self, number, record, fields):
        self.group_id = None
        self.transaction_count = None
        self.record_count = None
        self.currency_indicator = None
        self.total_monetary_value = None

        super(GroupTrailer, self).__init__(number, record, fields)

    def format_fields(self):
        super(GroupTrailer, self).format_fields()

        self.group_id.format('integer')
        self.transaction_count.format('integer')
        self.record_count.format('integer')
        self.total_monetary_value.format('integer')

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        self.transaction_count.format('integer')
        if self.transaction_count.value != len(group.transactions):
            group.group_reject('Transactions count does not match')

        # TODO
        # self.record_count.format('integer')
        # if self.record_count != len(group._transactions):
        # group.group_reject('Records count does not match')

        if self.total_monetary_value.value is not None and self.total_monetary_value.value > 0 \
                and self.currency_indicator.value is None:
            group.group_reject('Expected currency indicator with total monetary value present')

    def field_level_validation(self):
        pass

    def record_level_validation(self):
        pass


class Header(CWRObject):
    def __init__(self, number, record, fields):
        self.sender_type = None
        self.sender_id = None
        self.sender_name = None
        self.edi_standard_version_number = None
        self.creation_date = None
        self.creation_time = None
        self.transmission_date = None
        self.character_set = None

        super(Header, self).__init__(number, record, fields)

    def format_fields(self):
        super(Header, self).format_fields()

        self.sender_id.format('integer')
        self.creation_date.format('date')
        self.creation_time.format('time')
        self.transmission_date.format('date')

    def file_level_validation(self, document):
        if self.sender_type.check(SENDER_VALUES):
            document.reject(self, 'Invalid sender type')

        if self.sender_type.value in ['PB', 'WR', 'AA'] and self.sender_id.value is None:
            document.reject(self, 'Expected sender id')
        elif self.sender_type.value == 'OS' and self.sender_id.check(SOCIETY_CODES):
            document.reject(self, 'Invalid sender ID for society')

        if self.creation_date.rejected:
            document.reject(self, 'Invalid creation date')
        if self.transmission_date.rejected:
            document.reject(self, 'Invalid transmission date')

    def field_level_validation(self):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass

    def record_level_validation(self):
        pass


class InstrumentationDetails(CWRObject):
    def __init__(self, number, record, fields):
        self.instrument_code = None
        self.players_number = None

        super(InstrumentationDetails, self).__init__(number, record, fields)

    def format_fields(self):
        super(InstrumentationDetails, self).format_fields()

        self.players_number.format('integer')

    def field_level_validation(self):
        pass

    def record_level_validation(self):
        if self.instrument_code.check(INSTRUMENT_CODES, True):
            self.reject('Instrument code is not valid')
        if self.players_number.format('integer'):
            self.reject('Number of players must be numeric')

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass


class InstrumentationSummary(CWRObject):
    def __init__(self, number, record, fields):
        self.voices_number = None
        self.standard_instrumentation_type = None
        self.instrumentation_description = None

        super(InstrumentationSummary, self).__init__(number, record, fields)

    def format_fields(self):
        super(InstrumentationSummary, self).format_fields()

        self.voices_number.format('integer')

    def field_level_validation(self):
        pass

    def record_level_validation(self):
        pass

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass


class InterestedParty(CWRObject):
    def __init__(self, number, record, fields):
        self.agreement_role_code = None
        self.cae_ipi_id = None
        self.ipi_base_number = None
        self.id = None
        self.last_name = None
        self.writer_first_name = None
        self.pr_society = None
        self.pr_share = None
        self.mr_society = None
        self.mr_share = None
        self.sr_society = None
        self.sr_share = None

        self.nr_name = None
        super(InterestedParty, self).__init__(number, record, fields)

    def format_fields(self):
        super(InterestedParty, self).format_fields()

        self.pr_share.format('float')
        self.mr_share.format('float')
        self.sr_share.format('float')

    def transaction_level_validation(self, transaction):
        if self.agreement_role_code.value == 'AC' and \
                self.pr_share.value == self.mr_share.value == self.sr_share.value == 0:
            transaction.transaction_reject('Expected one of the shares greater than 0', self)

        if self.pr_share.value is not None and self.pr_share.value > 0 and self.pr_society.value is None:
            transaction.transaction_reject('Expected PR society', self)
        elif self.pr_society.check(SOCIETY_CODES, True):
            transaction.transaction_reject('PR Society code is not valid', self)
        if not 0 <= self.pr_share.value <= 100:
            transaction.transaction_reject('PR share must be between 0 and 100', self)
        if self.pr_share.value > 0 and self.pr_society.value is None:
            transaction.transaction_reject('Expected PR society with share greater than 0', self)

        if self.mr_share.value is not None and self.mr_share.value > 0 and self.mr_society.value is None:
            transaction.transaction_reject('Expected MR society', self)
        if self.mr_society.check(SOCIETY_CODES, True):
            transaction.transaction_reject('MR Society code is not valid', self)
        if not 0 <= self.mr_share.value <= 100:
            transaction.transaction_reject('MR share must be between 0 and 100', self)
        if self.mr_share.value > 0 and self.mr_society.value is None:
            transaction.transaction_reject('Expected MR society with share greater than 0', self)

        if self.sr_share.value is not None and self.sr_share.value > 0 and self.sr_society.value is None:
            transaction.transaction_reject('Expected SR society', self)
        if self.sr_society.check(SOCIETY_CODES, True):
            transaction.transaction_reject('SR Society code is not valid', self)
        if not 0 <= self.sr_share.value <= 100:
            transaction.transaction_reject('SR share must be between 0 and 100', self)
        if self.sr_share.value > 0 and self.sr_society.value is None:
            transaction.transaction_reject('Expected SR society with share greater than 0', self)

        if self.pr_society.value is None and self.mr_society.value is None:
            transaction.transaction_reject('Expected at least one of PR or MR society', self)

    def group_level_validation(self, group):
        pass

    def field_level_validation(self):
        if self.agreement_role_code.value != 'AS':
            self.writer_first_name.reject()

    def file_level_validation(self, document):
        pass

    def record_level_validation(self):
        pass


class NRPartyName(CWRObject):
    def __init__(self, number, record, fields):
        self.interested_party_id = None
        self.name = None
        self.writer_first_name = None
        self.language_code = None

        super(NRPartyName, self).__init__(number, record, fields)

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass

    def field_level_validation(self):
        self.language_code.check(LANGUAGE_CODES)

    def file_level_validation(self, document):
        pass

    def record_level_validation(self):
        pass


class NROtherWriterName(CWRObject):
    def __init__(self, number, record, fields):
        self.writer_name = None
        self.writer_first_name = None
        self.language_code = None
        self.writer_position = None

        super(NROtherWriterName, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def field_level_validation(self):
        self.language_code.check(LANGUAGE_CODES, True)
        self.writer_position.check(['1', '2'], True, '1')

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass

    def record_level_validation(self):
        if self.writer_name.value is None:
            self.reject('Expected writer name')


class NRPerformanceData(CWRObject):
    def __init__(self, number, record, fields):
        self.artist_name = None
        self.artist_first_name = None
        self.artist_ipi_cae_id = None
        self.artist_ipi_base_number = None
        self.language_code = None
        self.performance_language = None
        self.performance_dialect = None

        super(NRPerformanceData, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def record_level_validation(self):
        if self.artist_name.value is None and self.performance_language.value is None and \
                        self.performance_dialect.value is None:
            self.reject('Expected one of artist name, performance language or performance dialect')

    def field_level_validation(self):
        self.language_code.check(LANGUAGE_CODES, True)
        self.performance_language.check(LANGUAGE_CODES, True)

    def group_level_validation(self, group):
        pass

    def transaction_level_validation(self, transaction):
        pass


class NRPublisherName(CWRObject):
    def __init__(self, number, record, fields):
        self.publisher_sequence_id = None
        self.interested_party_id = None
        self.publisher_name = None
        self.language_code = None

        super(NRPublisherName, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def field_level_validation(self):
        self.language_code.check(LANGUAGE_CODES, True)

    def record_level_validation(self):
        if self.publisher_name.value is None:
            self.reject('Publisher name must be entered')

    def group_level_validation(self, group):
        pass


class NRSpecialTitle(CWRObject):
    def __init__(self, number, record, fields):
        self.title = None
        self.language_code = None

        super(NRSpecialTitle, self).__init__(number, record, fields)

    def transaction_level_validation(self, transaction):
        pass

    def record_level_validation(self):
        pass

    def field_level_validation(self):
        pass

    def group_level_validation(self, group):
        pass

    def file_level_validation(self, document):
        pass


class NRWorkTitle(CWRObject):
    def __init__(self, number, record, fields):
        self.title = None
        self.title_type = None
        self.language_code = None

        super(NRWorkTitle, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def field_level_validation(self):
        self.title_type.check(TITLE_TYPES, False, 'ALT')

    def record_level_validation(self):
        if self.language_code.check(LANGUAGE_CODES, True):
            self.reject('Invalid language code')

    def group_level_validation(self, group):
        pass


class NRWriterName(CWRObject):
    def __init__(self, number, record, fields):
        self.interested_party_id = None
        self.writer_name = None
        self.writer_first_name = None
        self.language_code = None

        super(NRWriterName, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def field_level_validation(self):
        if self.language_code.check(LANGUAGE_CODES, True):
            self.reject('Invalid language code')

    def record_level_validation(self):
        pass

    def group_level_validation(self, group):
        pass


class PerformingArtist(CWRObject):
    def __init__(self, number, record, fields):
        self.last_name = None
        self.first_name = None
        self.cae_ipi_name = None
        self.ipi_base_number = None

        super(PerformingArtist, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def field_level_validation(self):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass

    def record_level_validation(self):
        pass


class PublisherControl(CWRObject):
    def __init__(self, number, record, fields):
        self._territories = []
        self._administrators = {}
        self._sub_publishers = {}

        self._nr_name = None

        self.sequence_id = None
        self.interested_party_id = None
        self.name = None
        self.unknown_indicator = None
        self.type = None
        self.tax_id_number = None
        self.cae_ipi_name = None
        self.agreement_number = None
        self.pr_society = None
        self.pr_share = None
        self.mr_society = None
        self.mr_share = None
        self.sr_society = None
        self.sr_share = None
        self.reversionary_indicator = None
        self.first_recording_refusal_indicator = None
        self.ipi_base_number = None
        self.international_standard_agreement_code = None
        self.society_assigned_agreement_number = None
        self.agreement_type = None
        self.usa_licensed_indicator = None

        super(PublisherControl, self).__init__(number, record, fields)

    @property
    def nr_name(self):
        return self._nr_name

    @nr_name.setter
    def nr_name(self, nr_name):
        if self._last_record != 'SPU':
            nr_name.reject('Expected this record after a SPU record')
        if self.interested_party_id.value != nr_name.interested_party_id.value:
            nr_name.reject('Interested party id differs from the previous publisher interested party id')
        self._nr_name = nr_name

    def add_administrator(self, administrator):
        if self.type.value in ['E', 'PA', 'SE'] and administrator.type.value == 'AM':
            self._administrators[str(administrator.sequence_id.value)] = administrator
            self._last_record = administrator.record_type.value
        else:  # TODO: Raise exception
            pass

    def add_sub_publisher(self, sub_publisher):
        if self.type.value in ['E', 'PA'] and sub_publisher.type.value == 'SE':
            self._sub_publishers[str(sub_publisher.sequence_id.value)] = sub_publisher
            self._last_record = sub_publisher.record_type.value
        else:  # TODO: Raise exception
            pass

    def add_territory(self, territory):
        if self._last_record not in ['NPN', 'SPU', 'SPT']:
            self.reject('Unexpected territory record', territory)
        elif self.interested_party_id.value != territory.interested_party_id.value:
            self.reject('Interested party id does not correspond with previous SPU interested party id', territory)

        if self.record_type.value != 'SPU':
            territory.transaction_reject()

        if territory.sequence_id.value != (len(self._territories) + 1):
            territory.reject('Sequence number must be consecutive')

        self._territories.append(territory)
        self._last_record = territory.record_type.value

    def extract_records(self):
        records = []

        if self._nr_name is not None:
            records.append(self._nr_name)

        records.extend(self._territories)

        for admin in self._administrators.values():
            records.append(admin)
            records.extend(admin.extract_records())

        for sub_publisher in self._sub_publishers.values():
            records.append(sub_publisher)
            records.extend(sub_publisher.extract_records())

        return records

    def format_fields(self):
        super(PublisherControl, self).format_fields()

        self.sequence_id.format('integer')
        self.tax_id_number.format('integer')
        self.pr_share.format('float')
        self.mr_share.format('float')
        self.sr_share.format('float')

    def file_level_validation(self, document):
        for ter in self._territories:
            ter.file_level_validation(document)
        for adm in self._administrators.values():
            adm.file_level_validation(document)
        for pub in self._sub_publishers.values():
            pub.file_level_validation(document)

        if self._nr_name is not None:
            self._nr_name.file_level_validation(document)

    def group_level_validation(self, group):
        for ter in self._territories:
            ter.group_level_validation(group)
        for adm in self._administrators.values():
            adm.group_level_validation(group)
        for pub in self._sub_publishers.values():
            pub.group_level_validation(group)

        if self._nr_name is not None:
            self._nr_name.group_level_validation(group)

    def transaction_level_validation(self, transaction):
        for ter in self._territories:
            ter.transaction_level_validation(transaction)
        for adm in self._administrators.values():
            adm.transaction_level_validation(transaction)
        for pub in self._sub_publishers.values():
            pub.transaction_level_validation(transaction)

        if self._nr_name is not None:
            self._nr_name.transaction_level_validation(transaction)

        if self.type.value in ['AM', 'SE', 'PA'] and \
                not (self.pr_share.value == self.mr_share.value == self.sr_share.value == 0):
            transaction.transaction_reject('Ownership shares must be zero', self)

        if self.record_type.value == 'SPU':
            if self.interested_party_id.value is None:
                transaction.transaction_reject('Expected interested party id for SPU records', self)
            if self.type.value is None:
                transaction.transaction_reject('Expected publisher type', self)
            if self.type.check(PUBLISHER_TYPES):
                transaction.transaction_level_validation('Invalid publisher type', self)
            if self.unknown_indicator.value is not None:
                transaction.transaction_reject('Publisher unknown indicator must be blank', self)
        elif self.record_type.value == 'OPU':
            pass

        if (self.record_type.value == 'SPU' or self.unknown_indicator.value != 'Y') and self.name.value is None:
            transaction.transaction_reject('Expected publisher name', self)

        if self.pr_society.check(SOCIETY_CODES, True):
            transaction.transaction_reject('Invalid PR society', self)
        if self.pr_share.value > 50:
            transaction.transaction_reject('PR share must not exceed 50')
        if self.mr_society.check(SOCIETY_CODES, True):
            transaction.transaction_reject('Invalid MR society', self)
        if self.mr_share.value > 100:
            transaction.transaction_reject('MR share must not exceed 50')
        if self.sr_society.check(SOCIETY_CODES, True):
            transaction.transaction_reject('Invalid SR society', self)
        if self.sr_share.value > 100:
            transaction.transaction_reject('SR share must not exceed 50')

    def record_level_validation(self):
        for ter in self._territories:
            ter.record_level_validation()
        for adm in self._administrators.values():
            adm.record_level_validation()
        for pub in self._sub_publishers.values():
            pub.record_level_validation()

        if self._nr_name is not None:
            self._nr_name.record_level_validation()

    def field_level_validation(self):
        for ter in self._territories:
            ter.field_level_validation()
        for adm in self._administrators.values():
            adm.field_level_validation()
        for pub in self._sub_publishers.values():
            pub.field_level_validation()

        if self._nr_name is not None:
            self._nr_name.field_level_validation()

        if self.record_type.value == 'OPU':
            self.unknown_indicator.check(['Y', 'N'], False, 'N')

            if self.unknown_indicator.value == 'Y' and self.name.value is not None:
                self.name.reject()

            self.reversionary_indicator.reject()
            self.type.check(PUBLISHER_TYPES, False, 'E')

        self.reversionary_indicator.check(['Y', 'N', 'U'], True, None)
        self.first_recording_refusal_indicator.check(['Y', 'N'], True, None)
        self.agreement_type.check(AGREEMENT_TYPE_VALUES, True)


class PublisherTerritory(CWRObject):
    def __init__(self, number, record, fields):
        self.interested_party_id = None
        self.pr_share = None
        self.mr_share = None
        self.sr_share = None
        self.inclusion_exclusion_indicator = None
        self.tis_numeric_code = None
        self.shares_change = None
        self.sequence_id = None

        super(PublisherTerritory, self).__init__(number, record, fields)

    def format_fields(self):
        super(PublisherTerritory, self).format_fields()

        self.pr_share.format('float')
        self.mr_share.format('float')
        self.sr_share.format('float')
        self.sequence_id.format('integer')

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        if self.inclusion_exclusion_indicator.value == 'I' and \
                (self.pr_share.value == self.mr_share.value == self.sr_share.value == 0):
            transaction.transaction_reject('Included territory must have some share', self)

        if self.pr_share.value > 50:
            transaction.transaction_reject('PR share must not exceed 50')
        if self.mr_share.value > 100:
            transaction.transaction_reject('MR share must not exceed 100')
        if self.sr_share.value > 100:
            transaction.transaction_reject('SR share must not exceed 100')

        if self.tis_numeric_code.check(TIS_CODES):
            transaction.transaction_reject('Invalid TIS code', self)

        if self.inclusion_exclusion_indicator.check(['E', 'I']):
            transaction.transaction_reject('Invalid Inclusion Exclusion indicator', self)

    def field_level_validation(self):
        self.shares_change.check(['Y', 'N'], False, 'N')

    def record_level_validation(self):
        pass

    def group_level_validation(self, group):
        pass


class RecordingDetail(CWRObject):
    def __init__(self, number, record, fields):
        self.first_release_date = None
        self.first_release_duration = None
        self.first_album_title = None
        self.first_album_label = None
        self.first_release_catalog_id = None
        self.ean = None
        self.isrc = None
        self.recording_format = None
        self.recording_technique = None
        self.media_type = None

        super(RecordingDetail, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def field_level_validation(self):
        self.first_release_date.format('date')
        self.first_release_duration.format('time')

        self.recording_format.check(RECORDING_FORMAT, True, 'A')
        self.recording_technique.check(RECORDING_TECHNIQUE, True, 'U')
        self.media_type.check(MEDIA_TYPES, True)

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass

    def record_level_validation(self):
        if not any(field.value is not None for field in self.__dict__):
            self.reject('At least one of the fields expected to be submitted')


class Registration(CWRObject):
    def __init__(self, number, record, fields):
        self.records = []

        self._entire_work_title = None
        self._recording_details = None
        self._version_original_title = None
        self._work_origin = None

        self._additional_info = []
        self._alternative_titles = []
        self._components = []
        self._instrumentation_details = []
        self._instrumentation_summaries = []
        self._performing_artists = []
        self._publishers = {}
        self._writers = []
        self._origins = []

        self.title = None
        self.language_code = None
        self.submitter_id = None
        self.iswc = None
        self.copyright_date = None
        self.copyright_number = None
        self.musical_distribution_category = None
        self.duration = None
        self.recorded_indicator = None
        self.text_music_relationship = None
        self.composite_type = None
        self.version_type = None
        self.excerpt_type = None
        self.music_arrangement = None
        self.lyric_adaptation = None
        self.contact_name = None
        self.contact_id = None
        self.cwr_work_type = None
        self.grand_rights_indicator = None
        self.composite_component_count = None
        self.printed_edition_publication_date = None
        self.exceptional_clause = None
        self.opus_number = None
        self.catalogue_number = None
        self.priority_flag = None

        super(Registration, self).__init__(number, record, fields)

    @property
    def entire_work_title(self):
        return self._entire_work_title

    @entire_work_title.setter
    def entire_work_title(self, entire_work):
        if self.transaction_number.value != entire_work.transaction_number.value:
            entire_work.reject('Wrong transaction number')
        elif self._entire_work_title is None:
            self._entire_work_title = entire_work
            self._last_record = entire_work.record_type.value
        else:
            self.transaction_reject('More than one entire work titles found', entire_work)

    @property
    def recording_details(self):
        return self._recording_details

    @recording_details.setter
    def recording_details(self, details):
        if self.transaction_number.value != details.transaction_number.value:
            details.reject('Wrong transaction number')
        elif self._recording_details is None:
            self._recording_details = details
            self._last_record = details.record_type.value
        else:
            self.transaction_reject('More than one recording details found', details)

    @property
    def version_original_title(self):
        return self._version_original_title

    @version_original_title.setter
    def version_original_title(self, original_title):
        if self.transaction_number.value != original_title.transaction_number.value:
            original_title.reject('Wrong transaction number')
        elif self._version_original_title is None:
            self._version_original_title = original_title
            self._last_record = original_title.record_type.value
        else:
            self.transaction_reject('More than one version titles found', original_title)

    def add_additional_info(self, additional_info):
        if self.transaction_number.value != additional_info.transaction_number.value:
            additional_info.reject('Wrong transaction number')
        else:
            self._additional_info.append(additional_info)
            self._last_record = additional_info.record_type.value

    def add_alternative_title(self, alternative_title):
        if self.transaction_number.value != alternative_title.transaction_number.value:
            alternative_title.reject('Wrong transaction number')
        else:
            self._alternative_titles.append(alternative_title)
            self._last_record = alternative_title.record_type.value

    def add_component(self, component):
        if self.transaction_number.value != component.transaction_number.value:
            component.reject('Wrong transaction number')
        else:
            if self.composite_type.value is None:
                component.reject('Composite type not entered', self)

            self._components.append(component)
            self._last_record = component.record_type.value

    def add_instrumentation_detail(self, detail):
        if self.transaction_number.value != detail.transaction_number.value:
            detail.reject('Wrong transaction number')
        else:
            self._instrumentation_details.append(detail)
            self._last_record = detail.record_type.value

    def add_instrumentation_summary(self, summary):
        if self.transaction_number.value != summary.transaction_number.value:
            summary.reject('Wrong transaction number')
        else:
            self._instrumentation_summaries.append(summary)
            self._last_record = summary.record_type.value

    def add_performing_artist(self, artist):
        if self.transaction_number.value != artist.transaction_number.value:
            artist.reject('Wrong transaction number')
        else:
            self._performing_artists.append(artist)
            self._last_record = artist.record_type.value

    def add_publisher(self, publisher):
        if self.transaction_number.value != publisher.transaction_number.value:
            publisher.reject('Wrong transaction number')
        else:
            if publisher.type.value not in ['E', 'PA']:
                self.transaction_reject('First publisher in a chain must be original or income participant', publisher)
            self._publishers[str(publisher.sequence_id.value)] = publisher
            self._last_record = publisher.record_type.value

    def add_writer(self, writer):
        if self.transaction_number.value != writer.transaction_number.value:
            writer.reject('Wrong transaction number')
        else:
            self._writers.append(writer)
            self._last_record = writer.record_type.value

    def add_origin(self, origin):
        if self.transaction_number.value != origin.transaction_number.value:
            origin.reject('Wrong transaction number')
        else:
            self._origins.append(origin)
            self._last_record = origin.record_type.value

    def extract_records(self):
        records = []

        if self._entire_work_title is not None:
            records.append(self._entire_work_title)
        if self._recording_details is not None:
            records.append(self._recording_details)
        if self._version_original_title is not None:
            records.append(self._version_original_title)
        if self._work_origin is not None:
            records.append(self._work_origin)

        records.extend(self._additional_info)
        records.extend(self._alternative_titles)
        records.extend(self._components)
        records.extend(self._instrumentation_details)
        records.extend(self._instrumentation_summaries)
        records.extend(self._performing_artists)

        for publisher in self._publishers.values():
            records.append(publisher)
            records.extend(publisher.extract_records())

        for writer in self._writers:
            records.append(writer)
            records.extend(writer.extract_records())

        records.extend(self._origins)

        self.records = records


        return records

    def format_fields(self):
        super(Registration, self).format_fields()

        self.copyright_date.format('date')
        self.duration.format('time')
        self.composite_component_count.format('integer')
        self.printed_edition_publication_date.format('date')

    def transaction_level_validation(self, transaction):
        if self._entire_work_title is not None:
            self._entire_work_title.transaction_level_validation(self)
        if self._recording_details is not None:
            self._recording_details.transaction_level_validation(self)
        if self._version_original_title is not None:
            self._version_original_title.transaction_level_validation(self)
        if self._work_origin is not None:
            self._work_origin.transaction_level_validation(self)

        for ari in self._additional_info:
            ari.transaction_level_validation(self)
        for alt in self._alternative_titles:
            alt.transaction_level_validation(self)
        for com in self._components:
            com.transaction_level_validation(self)
        for ind in self._instrumentation_details:
            ind.transaction_level_validation(self)
        for ins in self._instrumentation_summaries:
            ins.transaction_level_validation(self)
        for per in self._performing_artists:
            per.transaction_level_validation(self)
        for pub in self._publishers:
            pub.transaction_level_validation(self)
        for wri in self._writers:
            wri.transaction_level_validation(self)
        for ori in self._origins:
            ori.transaction_level_validation(self)

        if self.musical_distribution_category.value == 'SER' and len(self._instrumentation_summaries) == 0:
            self.transaction_reject('Expected one instrumentation summary at least')

        total_pub_pr_share = sum(pub.pr_share.value for pub in self._publishers)
        total_pub_mr_share = sum(pub.mr_share.value for pub in self._publishers)
        total_pub_sr_share = sum(pub.sr_share.value for pub in self._publishers)
        if total_pub_pr_share > 50:
            self.transaction_reject('PR share across all publishers must be 50 os less')
        if total_pub_mr_share > 100:
            self.transaction_reject('MR share across all publishers must be 100 os less')
        if total_pub_sr_share > 100:
            self.transaction_reject('SR share across all publishers must be 100 os less')

        total_wri_pr_share = sum(wri.pr_share.value for wri in self._writers)
        total_wri_mr_share = sum(wri.mr_share.value for wri in self._writers)
        total_wri_sr_share = sum(wri.sr_share.value for wri in self._writers)
        if total_wri_pr_share > 50:
            self.transaction_reject('PR share across all writers must be 50 os less')
        if total_wri_mr_share > 100:
            self.transaction_reject('MR share across all writers must be 100 os less')
        if total_wri_sr_share > 100:
            self.transaction_reject('SR share across all writers must be 100 os less')

        if total_pub_pr_share + total_wri_pr_share != 100:
            self.transaction_level_validation('The total PR share must be 100')
        if total_pub_mr_share + total_wri_mr_share != 100:
            self.transaction_level_validation('The total MR share must be 100')
        if total_pub_sr_share + total_wri_sr_share != 100:
            self.transaction_level_validation('The total SR share must be 100')

        if len(self._writers) == 0:
            self.transaction_reject('Expected at least one writer within the transaction')
        else:
            if self.version_type.value == 'MOD' and not any(
                    wri.designation_code.value in ['AR', 'AD', 'SR', 'SA', 'TR'] for wri in self._writers):
                self.transaction_reject('Not writers designation code required for MOD version type')

            if not any(wri.designation_code.value in ['CA', 'A', 'C'] for wri in self._writers):
                self.transaction_reject('Not writer designation code required for work registration')

            if self.version_type.value == 'ORI' and any(
                    wri.designation_code.value in ['AD', 'AR', 'SD'] for wri in self._writers):
                self.transaction_reject('Invalid writer designation code for ORI version type')

        if self.musical_distribution_category.check(DISTRIBUTION_CATEGORY_TABLE):
            self.transaction_reject('Invalid musical distribution category')
        if self.duration.rejected:
            self.transaction_reject('Duration must be a valid combination of hours, minutes and seconds')
        if self.musical_distribution_category.value == 'SER' and self.duration.value is None:
            self.transaction_reject('Duration must be greater than 0 for SER distribution category')
        if self.version_type.check(VERSION_TYPES):
            self.transaction_reject('Invalid version type')

        if self.version_type.value == 'MOD':
            if self.music_arrangement.check(MUSIC_ARRANGEMENT_TYPES):
                self.transaction_reject('Invalid music arrangement type for MOD version')
            if self.lyric_adaptation.check(LYRIC_ADAPTATION):
                self.transaction_reject('Invalid lyric adaptation type for MOD version')

        if self.composite_type.value is not None and self.composite_component_count.value is None:
            self.transaction_reject('Composite component count must be entered')
        if self.composite_component_count.value is not None and self.composite_component_count.value < 1:
            self.transaction_reject('Composite component count must be greater than 0')

        if self.music_arrangement.check(MUSIC_ARRANGEMENT_TYPES, True):
            self.transaction_reject('Invalid music arrangement type')
        if self.lyric_adaptation.check(LYRIC_ADAPTATION, True):
            self.transaction_reject('Invalid lyric adaptation type')

    def field_level_validation(self):
        if self._entire_work_title is not None:
            self._entire_work_title.field_level_validation()
        if self._recording_details is not None:
            self._entire_work_title.field_level_validation()
        if self._version_original_title is not None:
            self._version_original_title.field_level_validation()
        if self._work_origin is not None:
            self._work_origin.field_level_validation()

        for ari in self._additional_info:
            ari.field_level_validation()
        for alt in self._alternative_titles:
            alt.field_level_validation()
        for com in self._components:
            com.field_level_validation()
        for ind in self._instrumentation_details:
            ind.field_level_validation()
        for ins in self._instrumentation_summaries:
            ins.field_level_validation()
        for per in self._performing_artists:
            per.field_level_validation()
        for pub in self._publishers:
            pub.field_level_validation()
        for wri in self._writers:
            wri.field_level_validation()
        for ori in self._origins:
            ori.field_level_validation()

        if self.language_code.check(LANGUAGE_CODES, True):
            self.transaction_reject('Invalid language code for transaction')

        self.recorded_indicator.check(['Y', 'N', 'U'], 'U')
        self.text_music_relationship.check(TEXT_MUSIC_TABLE, True)
        self.composite_type.check(COMPOSITE_TYPE, True)
        self.excerpt_type.check(EXCERPT_TYPE, True)
        self.cwr_work_type.check(WORK_TYPES, True)
        self.exceptional_clause.check(['Y', 'N', 'U'], True, 'U')

    def file_level_validation(self, document):
        if self._entire_work_title is not None:
            self._entire_work_title.file_level_validation(document)
        if self._recording_details is not None:
            self._recording_details.file_level_validation(document)
        if self._version_original_title is not None:
            self._version_original_title.file_level_validation(document)
        if self._work_origin is not None:
            self._work_origin.file_level_validation(document)

        for ari in self._additional_info:
            ari.file_level_validation(document)
        for alt in self._alternative_titles:
            alt.file_level_validation(document)
        for com in self._components:
            com.file_level_validation(document)
        for ind in self._instrumentation_details:
            ind.file_level_validation(document)
        for ins in self._instrumentation_summaries:
            ins.file_level_validation(document)
        for per in self._performing_artists:
            per.file_level_validation(document)
        for pub in self._publishers.values():
            pub.file_level_validation(document)
        for wri in self._writers:
            wri.file_level_validation(document)
        for ori in self._origins:
            ori.file_level_validation(document)

    def group_level_validation(self, group):
        if self._entire_work_title is not None:
            self._entire_work_title.group_level_validation(group)
        if self._recording_details is not None:
            self._recording_details.group_level_validation(group)
        if self._version_original_title is not None:
            self._version_original_title.group_level_validation(group)
        if self._work_origin is not None:
            self._work_origin.group_level_validation(group)

        for ari in self._additional_info:
            ari.group_level_validation(group)
        for alt in self._alternative_titles:
            alt.group_level_validation(group)
        for com in self._components:
            com.group_level_validation(group)
        for ind in self._instrumentation_details:
            ind.group_level_validation(group)
        for ins in self._instrumentation_summaries:
            ins.group_level_validation(group)
        for per in self._performing_artists:
            per.group_level_validation(group)
        for pub in self._publishers.values():
            pub.group_level_validation(group)
        for wri in self._writers:
            wri.group_level_validation(group)
        for ori in self._origins:
            ori.group_level_validation(group)

    def record_level_validation(self):
        if self._entire_work_title is not None:
            self._entire_work_title.record_level_validation()
        if self._recording_details is not None:
            self._recording_details.record_level_validation()
        if self._version_original_title is not None:
            self._version_original_title.record_level_validation()
        if self._work_origin is not None:
            self._work_origin.record_level_validation()

        for ari in self._additional_info:
            ari.record_level_validation()
        for alt in self._alternative_titles:
            alt.record_level_validation()
        for com in self._components:
            com.record_level_validation()
        for ind in self._instrumentation_details:
            ind.record_level_validation()
        for ins in self._instrumentation_summaries:
            ins.record_level_validation()
        for per in self._performing_artists:
            per.record_level_validation()
        for pub in self._publishers:
            pub.record_level_validation()
        for wri in self._writers:
            wri.record_level_validation()

        for agent in wri.agents():
            if not any(pub.interested_party_id.value == agent.ip_id.value for pub in self._publishers):
                agent.reject('IP value not correspond to any of the previous publishers')
        for ori in self._origins:
            ori.record_level_validation()

    def transaction_reject(self, msg_text, record=None):
        rejection_record = self if record is None else record
        super(Registration, self).reject(msg_text, rejection_record, CWRMessage.TYPES.TRANSACTION,
                                         CWRMessage.TYPES.TRANSACTION)


class Territory(CWRObject):
    def __init__(self, number, record, fields):
        self.inclusion_exclusion_indicator = None
        self.tis_numeric_code = None

        super(Territory, self).__init__(number, record, fields)

    def transaction_level_validation(self, transaction):
        if self.tis_numeric_code.check(TIS_CODES):
            transaction.transaction_reject('Invalid TIS numeric code', self)

    def file_level_validation(self, document):
        pass

    def record_level_validation(self):
        pass

    def group_level_validation(self, group):
        pass

    def field_level_validation(self):
        pass


class Trailer(CWRObject):
    def __init__(self, number, record, fields):
        self.group_count = None
        self.transaction_count = None
        self.record_count = None

        super(Trailer, self).__init__(number, record, fields)

    def format_fields(self):
        super(Trailer, self).format_fields()

        self.group_count.format('integer')
        self.transaction_count.format('integer')
        self.record_count.format('integer')

    def file_level_validation(self, document):
        pass

    def field_level_validation(self):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass

    def record_level_validation(self):
        pass


class WorkAdditionalInfo(CWRObject):
    def __init__(self, number, record, fields):
        self.society_id = None
        self.work_id = None
        self.right_type = None
        self.subject_code = None
        self.note = None

        super(WorkAdditionalInfo, self).__init__(number, record, fields)

    def transaction_level_validation(self, transaction):
        pass

    def file_level_validation(self, document):
        pass

    def record_level_validation(self):
        if self.society_id.check(SOCIETY_CODES):
            self.reject('Invalid society code')

        if self.right_type.check(RIGHT_TYPES):
            self.reject('Invalid right type')

        if self.note is not None and self.subject_code.check(SUBJECT_CODES):
            self.reject('Invalid subject code')

    def group_level_validation(self, group):
        pass

    def field_level_validation(self):
        pass


class WorkAlternativeTitle(CWRObject):
    def __init__(self, number, record, fields):
        self.alternate_title = None
        self.title_type = None
        self.language_code = None

        super(WorkAlternativeTitle, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        self.alternate_title.check(TITLE_TYPES, False, 'ALT')

    def transaction_level_validation(self, transaction):
        pass

    def field_level_validation(self):
        pass

    def record_level_validation(self):
        if self.language_code.check(LANGUAGE_CODES, True):
            self.reject('Invalid language code')

    def group_level_validation(self, group):
        pass


class WorkComponent(CWRObject):
    def __init__(self, number, record, fields):
        self.title = None
        self.iswc = None
        self.submitter_id = None
        self.duration = None
        self.writer_one_last_name = None
        self.writer_one_first_name = None
        self.writer_one_ipi_cae = None
        self.writer_one_ipi_base_number = None
        self.writer_two_last_name = None
        self.writer_two_first_name = None
        self.writer_two_ipi_cae = None
        self.writer_two_ipi_base_number = None

        super(WorkComponent, self).__init__(number, record, fields)

    def format_fields(self):
        super(WorkComponent, self).format_fields()

        self.duration.format('time')

    def transaction_level_validation(self, transaction):
        pass

    def file_level_validation(self, document):
        pass

    def record_level_validation(self):
        pass

    def group_level_validation(self, group):
        pass

    def field_level_validation(self):
        if self.writer_two_first_name.value is not None and self.writer_two_last_name.value is None:
            self.writer_two_first_name.reject()
            self.writer_two_last_name.reject()


class WorkExcerptTitle(CWRObject):
    def __init__(self, number, record, fields):
        self.entire_title = None
        self.entire_work_iswc = None
        self.language_code = None
        self.writer_one_last_name = None
        self.writer_one_first_name = None
        self.writer_one_ipi_cae = None
        self.writer_one_ipi_base_number = None
        self.writer_two_last_name = None
        self.writer_two_first_name = None
        self.writer_two_ipi_cae = None
        self.writer_two_ipi_base_number = None
        self.submitter_id = None

        super(WorkExcerptTitle, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def field_level_validation(self):
        self.language_code.check(LANGUAGE_CODES, True)

    def record_level_validation(self):
        pass

    def group_level_validation(self, group):
        pass


class WorkOrigin(CWRObject):
    def __init__(self, number, record, fields):
        self.intended_purpose = None
        self.production_title = None
        self.cd_identifier = None
        self.cut_number = None
        self.library = None
        self.blt = None
        self.visan_version = None
        self.visan_isan = None
        self.visan_episode = None
        self.visan_check_digit = None
        self.production_id = None
        self.episode_title = None
        self.episode_id = None
        self.production_year = None
        self.avi_key_society = None
        self.avi_key_number = None

        super(WorkOrigin, self).__init__(number, record, fields)

    def format_fields(self):
        super(WorkOrigin, self).format_fields()

        self.cut_number.format('integer')
        self.visan_version.format('integer')
        self.visan_isan.format('integer')
        self.visan_episode.format('integer')
        self.visan_check_digit.format('integer')
        self.production_year.format('integer')
        self.avi_key_society.format('integer')

    def file_level_validation(self, document):
        pass

    def field_level_validation(self):
        if self.cd_identifier.value is None or self.cut_number is None:
            self.cd_identifier.reject()
            self.cut_number.reject()

        self.blt.check(['B', 'L', 'T'], True)

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass

    def record_level_validation(self):
        if self.intended_purpose.check(INTENDED_PURPOSES, False):
            self.reject('Invalid intended purpose')

        if self.intended_purpose.value == 'LIB' and self.cd_identifier is None:
            self.reject('CD identifier is required')

        if self.production_title.value is None and self.library.value is None:
            self.reject('Production title or library must be entered')


class WorkVersionTitle(CWRObject):
    def __init__(self, number, record, fields):
        self.entire_title = None
        self.entire_work_iswc = None
        self.language_code = None
        self.writer_one_last_name = None
        self.writer_one_first_name = None
        self.writer_one_ipi_cae = None
        self.writer_one_ipi_base_number = None
        self.writer_two_last_name = None
        self.writer_two_first_name = None
        self.writer_two_ipi_cae = None
        self.writer_two_ipi_base_number = None
        self.submitter_id = None

        super(WorkVersionTitle, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def field_level_validation(self):
        self.language_code.check(LANGUAGE_CODES, True)

    def transaction_level_validation(self, transaction):
        pass

    def group_level_validation(self, group):
        pass

    def record_level_validation(self):
        pass


class WriterAgent(CWRObject):
    def __init__(self, number, record, fields):
        self.ip_id = None
        self.name = None
        self.agreement_number = None
        self.society_assigned_number = None
        self.writer_ip_id = None

        super(WriterAgent, self).__init__(number, record, fields)

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        pass

    def field_level_validation(self):
        pass

    def record_level_validation(self):
        pass

    def group_level_validation(self, group):
        pass


class WriterControl(CWRObject):
    def __init__(self, number, record, fields):
        self._territories = {}
        self._agents = []

        self._nr_name = None

        self.interested_party_id = None
        self.last_name = None
        self.first_name = None
        self.unknown_indicator = None
        self.designation_code = None
        self.tax_id_number = None
        self.cae_ipi_name_id = None
        self.pr_society = None
        self.pr_share = None
        self.mr_society = None
        self.mr_share = None
        self.sr_society = None
        self.sr_share = None
        self.reversionary_indicator = None
        self.first_recording_refusal_indicator = None
        self.work_for_hire_indicator = None
        self.ipi_base_number = None
        self.personal_number = None
        self.usa_license_indicator = None

        super(WriterControl, self).__init__(number, record, fields)

    @property
    def nr_name(self):
        return self._nr_name

    @nr_name.setter
    def nr_name(self, nr_name):
        if self._last_record != 'SWR':
            nr_name.reject('Expected previous record to be SWR')

        self._nr_name = nr_name
        self._last_record = nr_name.record_type.value

    def add_agent(self, agent):
        if self.record_type.value == 'OWR':
            agent.transaction_reject()
        elif self._last_record not in ['SWR', 'SWT', 'PWR']:
            agent.transaction_reject()

        self._agents.append(agent)
        self._last_record = agent.record_type.value

    def add_territory(self, territory):
        if self._last_record not in ['SWR', 'SWT', 'NWN']:
            self.reject('Unexpected territory record', territory)

        if self.record_type == 'OWR':
            territory.transaction_reject()
        elif territory.interested_party_id.value != self.interested_party_id.value:
            territory.reject('Writer interested party id not correspond to previous writer interested party id')

        if territory.tis_numeric_code.value not in self._territories.keys():
            self._territories[territory.tis_numeric_code.value] = territory
            self._last_record = territory.record_type.value
        else:
            territory.reject('Duplicated tis code for given writer')

    def extract_records(self):
        records = []

        if self._nr_name is not None:
            records.append(self._nr_name)

        records.extend(self._territories.values())
        records.extend(self._agents)

        return records

    def format_fields(self):
        super(WriterControl, self).format_fields()

        self.tax_id_number.format('integer')
        self.pr_share.format('float')
        self.mr_share.format('float')
        self.sr_share.format('float')
        self.personal_number.format('integer')

    def file_level_validation(self, document):
        for agent in self._agents:
            agent.file_level_validation(document)
        for territory in self._territories.values():
            territory.file_level_validation(document)

        if self._nr_name is not None:
            self._nr_name.file_level_validation(document)

    def transaction_level_validation(self, transaction):
        for agent in self._agents:
            agent.transaction_level_validation(transaction)
        for territory in self._territories.values():
            territory.transaction_level_validation(transaction)

        if self._nr_name is not None:
            self._nr_name.transaction_level_validation(transaction)

        if self.pr_share.value != self.mr_share.value != self.sr_share.value != 100 and len(self._agents) == 0:
            transaction.transaction_reject('Expected agent for writer for an unpublished work', self)

        if self.record_type.value == 'SWR':
            if self.interested_party_id.value is None:
                transaction.transaction_reject('Expected interested party ID for SWR record', self)
            if self.unknown_indicator.value != 'Y' and self.last_name.value is None:
                transaction.transaction_reject('Expected writer last name', self)
            if self.unknown_indicator.value is not None:
                transaction.transaction_reject('Writer unknown indicator must be blank', self)
            if self.designation_code.value is None:
                transaction.transaction_reject('Expected writer designation code', self)

        if self.designation_code.check(WRITER_DESIGNATIONS, True):
            transaction.transaction_reject('Invalid writer designation code', self)

        if self.pr_society.check(SOCIETY_CODES, True):
            transaction.transaction_reject('Invalid PR society code', self)
        if self.pr_share.value > 100:
            transaction.transaction_reject('PR share must be between 0 and 100', self)
        if self.mr_society.check(SOCIETY_CODES, True):
            transaction.transaction_reject('Invalid MR society code', self)
        if self.mr_share.value > 100:
            transaction.transaction_reject('MR share must be between 0 and 100', self)
        if self.sr_society.check(SOCIETY_CODES, True):
            transaction.transaction_reject('Invalid SR society code', self)
        if self.sr_share.value > 100:
            transaction.transaction_reject('SR share must be between 0 and 100', self)

    def field_level_validation(self):
        for agent in self._agents:
            agent.field_level_validation()
        for territory in self._territories.values():
            territory.field_level_validation()

        if self._nr_name is not None:
            self._nr_name.field_level_validation()

        if self.record_type.value == 'OWR':
            self.unknown_indicator.check(['Y', 'N'], True, 'N')

            if self.unknown_indicator.value == 'Y':
                self.last_name.reject()

        self.reversionary_indicator.check(['Y', 'N', 'U'], True)
        self.first_recording_refusal_indicator.check(['Y', 'N'], True)
        self.work_for_hire_indicator.check(['Y', 'N'], True)

    def record_level_validation(self):
        for agent in self._agents:
            agent.record_level_validation()
        for territory in self._territories.values():
            territory.record_level_validation()

        if self._nr_name is not None:
            self._nr_name.record_level_validation()

    def group_level_validation(self, group):
        for agent in self._agents:
            agent.group_level_validation(group)
        for territory in self._territories.values():
            territory.group_level_validation(group)

        if self._nr_name is not None:
            self._nr_name.group_level_validation(group)


class WriterTerritory(CWRObject):
    def __init__(self, number, record, fields):
        self.interested_party_id = None
        self.pr_share = None
        self.mr_share = None
        self.sr_share = None
        self.inclusion_exclusion_indicator = None
        self.tis_numeric_code = None
        self.shares_change = None
        self.sequence_id = None

        super(WriterTerritory, self).__init__(number, record, fields)

    def format_fields(self):
        super(WriterTerritory, self).format_fields()

        self.pr_share.format('float')
        self.mr_share.format('float')
        self.sr_share.format('float')
        self.sequence_id.format('integer')

    def file_level_validation(self, document):
        pass

    def transaction_level_validation(self, transaction):
        if self.inclusion_exclusion_indicator.value == 'I' and \
                self.pr_share.value == self.mr_share.value == self.sr_share.value == 0:
            transaction.transaction_reject('Expected at least one share to be greater than 0', self)

        if self.pr_share.value > 100:
            transaction.transaction_reject('PR share must be between 0 and 100', self)
        if self.mr_share.value > 100:
            transaction.transaction_reject('MR share must be between 0 and 100', self)
        if self.sr_share.value > 100:
            transaction.transaction_reject('SR share must be between 0 and 100', self)

        if self.tis_numeric_code.check(TIS_CODES):
            transaction.transaction_reject('Invalid TIS numeric code', self)
        if self.inclusion_exclusion_indicator.check(['E', 'I']):
            transaction.transaction_reject('Invalid inclusion exclusion indicator', self)

    def field_level_validation(self):
        self.shares_change.check(['Y', 'N'], True, 'N')

    def record_level_validation(self):
        pass

    def group_level_validation(self, group):
        pass