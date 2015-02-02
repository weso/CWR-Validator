from models.document import Document
from models.records import Record

__author__ = 'Borja'


class Validator(object):

    def __init__(self):
        self._document = Document()

        self._records = []
        self._malformed_records = []

    @property
    def document(self):
        return self._document

    def validate_document(self, document_json):
        self._document = Document()

        self.validate_document_format(document_json)
        self.validate_document_structure()
        self._document.validate()

        return self._document

    def validate_document_format(self, document_json):
        """
        Validate an entire document record by record, checking if they are well formed.
        Also prepares the validator for the next step in a complete document validation.
        :param document_json: Expected an array representing the document records
        :return: Both arrays, first one containing the valid records and second one with the failures
        """
        valid_records = []
        invalid_records = []

        for index, record in enumerate(document_json):
            record_object = Record.factory(record.replace('\n', '').replace('\r', ''))

            if record_object.check_format_with_regex():
                valid_records.append(record)
                self._records.append(record_object.promote(index))
            else:
                invalid_records.append(record)
                self._malformed_records.append(record)

        return valid_records, invalid_records

    def validate_document_structure(self):

        while self._records:

            # New record to evaluate whether or not is well positioned
            record = self._records.pop(0)
            record_type = str(record.record_type)

            if record_type == 'HDR':
                self._document.header = record
            elif record_type == 'TRL':
                self._document.trailer = record
            elif record_type == 'GRH':

                # If a group starts the validation goes to a new level
                self._document.add_group(self._validate_group(record))
            else:  # TODO: Exception
                pass

    def _validate_group(self, group):
        from models.cwr_objects import CWRMessage

        group = group

        while self._records:
            record = self._records.pop(0)
            record_type = str(record.record_type)

            if record_type == 'GRT':
                group.add_trailer(record)

                return group
            elif record_type == 'AGR':
                group.add_transaction(self._validate_agreement(record))
            elif record_type in ['NWR', 'REV']:
                group.add_transaction(self._validate_registration(record))
            else:
                group.transaction_reject(CWRMessage.TYPES.GROUP, CWRMessage.TYPES.GROUP,
                                         'Encountered unexpected record type inside the group')

    def _validate_agreement(self, agreement):
        agreement = agreement

        while self._records:
            record_type = self._records[0].record_type.value

            # Now we don't pop the element as it can be a new transaction
            if record_type in ['IPA', 'NPA']:
                record = self._records.pop(0)
                agreement.add_interested_party(record)
            elif record_type == 'TER':
                record = self._records.pop(0)
                agreement.add_territory(record)
            else:
                return agreement

    def _validate_registration(self, registration):
        registration = registration

        while self._records:
            record_type = self._records[0].record_type.value

            # Now we don't pop the element as it can be a new transaction
            if record_type in ['SPU', 'OPU']:
                record = self._records.pop(0)
                registration.add_publisher(self._validate_publisher(record))
            elif record_type in ['SWR', 'OWR']:
                record = self._records.pop(0)
                registration.add_writer(self._validate_writer(record))
            elif record_type in ['ALT', 'NAT']:
                record = self._records.pop(0)
                registration.add_alternative_title(record)
            elif record_type in ['EWT', 'NET']:
                record = self._records.pop(0)
                registration.entire_work_title = record
            elif record_type in ['VER', 'NVT']:
                record = self._records.pop(0)
                registration.version_original_title = record
            elif record_type in ['PER', 'NPR']:
                record = self._records.pop(0)
                registration.add_performing_artist(record)
            elif record_type == 'REC':
                record = self._records.pop(0)
                registration.recording_details = record
            elif record_type == 'ORN':
                record = self._records.pop(0)
                registration.add_origin(record)
            elif record_type == 'INS':
                record = self._records.pop(0)
                registration.add_instrumentation_summary(record)
            elif record_type == 'IND':
                record = self._records.pop(0)
                registration.add_instrumentation_detail(record)
            elif record_type in ['COM', 'NCT']:
                record = self._records.pop(0)
                registration.add_component(record)
            elif record_type == 'ARI':
                record = self._records.pop(0)
                registration.add_additional_info(record)
            else:
                return registration

    def _validate_publisher(self, publisher):
        publisher = publisher

        while self._records:
            record_type = self._records[0].record_type.value

            if record_type in ['SPU', 'OPU']:
                if self._records[0].sequence_id.value != publisher.sequence_id.value:

                    # This means the chain has been changed
                    return publisher

                record = self._records.pop(0)

                if record.type.value == 'AM':
                    publisher.add_administrator(self._validate_publisher(record))
                elif record.type.value == 'SE':
                    publisher.add_sub_publisher(self._validate_publisher(record))
            elif record_type == 'SPT':
                record = self._records.pop(0)
                publisher.add_territory(record)
            elif record_type == 'NPN':
                record = self._records.pop(0)
                publisher.nr_name = record
            else:
                return publisher

    def _validate_writer(self, writer):
        writer = writer

        while self._records:
            record_type = self._records[0].record_type.value

            if record_type == 'NWN':
                record = self._records.pop(0)
                writer.nr_name = record
            elif record_type == 'SWT':
                record = self._records.pop(0)
                writer.add_territory(record)
            elif record_type == 'PWR':
                record = self._records.pop(0)
                writer.agent = record
            else:
                return writer