__author__ = 'Borja'
import abc
import datetime
import re


class Record(object):
    __metaclass__ = abc.ABCMeta

    FIELD_NAMES = []
    FIELD_REGEX = []
    FIELD_VALUES = []

    def __init__(self, record):
        self.FIELD_VALUES = []
        if record is None or record == '':
            raise ValueError("REGEX ERROR: Expected record couldn't be None")

        self._record = record
        self._regex = self._generate_regex()
        matcher = re.compile(self._regex)
        if matcher.match(record):
            self._build_record(record)
            if len(self.FIELD_NAMES) != len(self.FIELD_VALUES):
                raise ValueError("PARSE ERROR: Extracted values number {} must correspond with field names given {}"
                                 .format(len(self.FIELD_VALUES), len(self.FIELD_NAMES)))

            self._attr_dict = self._build_attr_dict()
            self.validate()
        else:
            self._check_regex_fields()

    @property
    def attr_dict(self):
        return self._attr_dict

    @abc.abstractmethod
    def _build_record(self, record):
        """ This method should build the record object related
            by reading the line in the CWR and validating the fields"""
        return

    @abc.abstractmethod
    def validate(self):
        """ This method must validate the fields in the record
            object according to it's field validation level"""
        return

    def _build_attr_dict(self):
        return dict(zip(self.FIELD_NAMES, self.FIELD_VALUES))

    def _check_regex_fields(self):
        start = 0
        for i, regex in enumerate(self.FIELD_REGEX):
            matcher = re.compile(str(regex))
            if not matcher.match(self._record[start:start+regex.size]):
                raise ValueError('REGEX ERROR: Record field {} does not validate with expression given {}'.format(
                    self.FIELD_NAMES[i], self._record[start:start+regex.size]))
            else:
                start += regex.size

    def _generate_regex(self):
        return '^' + "".join(str(regex) for regex in self.FIELD_REGEX) + '$'

    def extract_date_value(self, starts, size):
        value = self.get_value(starts, size)
        try:
            self.FIELD_VALUES.append(datetime.datetime.strptime(value, '%Y%m%d').date() if value else None)
        except ValueError:
            return None

    def extract_integer_value(self, starts, size):
        value = self.get_value(starts, size)
        self.FIELD_VALUES.append(int(value) if value else None)

    def extract_float_value(self, starts, size, integer_part_size):
        value = self.get_value(starts, size)
        try:
            self.FIELD_VALUES.append(float(
                value[0:0 + integer_part_size] + '.' + value[0 + integer_part_size:size]) if value else None)
        except ValueError:
            return None

    def extract_time_value(self, starts, size):
        value = self.get_value(starts, size)
        try:
            self.FIELD_VALUES.append(datetime.datetime.strptime(value, '%H%M%S').time() if value else None)
        except ValueError:
            return None

    def extract_value(self, starts, size):
        self.FIELD_VALUES.append(self.get_value(starts, size))

    def get_value(self, starts, size):
        value = self._record[starts:starts + size].strip()
        return value if value else None

    def __str__(self):
        return str(self._attr_dict)

    def __repr__(self):
        return self.__str__()