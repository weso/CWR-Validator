__author__ = 'Borja'
import abc
import datetime
import re

from validator.domain.exceptions.regex_error import RegexError


class Record(object):
    __metaclass__ = abc.ABCMeta

    FIELD_NAMES = []
    FIELD_REGEX = []
    FIELD_VALUES = []

    def __init__(self, record):
        self.FIELD_VALUES = []
        if record is None or record == '':
            raise ValueError("Record can't be None")

        self._record = record
        self._regex, self._regex_size = self._generate_regex()
        matcher = re.compile(str(self._regex))
        if matcher.match(record[0:self._regex_size]):
            self._build_record(record)
            self._attr_dict = self._build_attr_dict()
            self.format()
            self.validate()
        else:
            self._check_regex_fields()

    @property
    def attr_dict(self):
        return self._attr_dict

    @property
    def record(self):
        return str(self._record)

    def _build_record(self, record):
        start = 0
        for regex in self.FIELD_REGEX:
            self.extract_value(start, regex.size)
            start += regex.size

    @abc.abstractmethod
    def format(self):
        """ This method must give format to non string values """
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
            if not matcher.match(self._record[start:start + regex.size]):
                raise RegexError(self.FIELD_NAMES[i], str(regex), self._record[start:start + regex.size])
            else:
                if self._record[0:3] == 'HDR':
                    print "matches {} with {}".format(self._record[start:start + regex.size], str(regex))
                start += regex.size

    def _generate_regex(self):
        return '^' + "".join(str(regex) for regex in self.FIELD_REGEX) + '$', \
               sum(regex.size for regex in self.FIELD_REGEX)

    def format_date_value(self, field):
        value = self._attr_dict[field]
        try:
            if int(value) != 0:
                self._attr_dict[field] = datetime.datetime.strptime(value, '%Y%m%d').date() if value else None
            else:
                self._attr_dict[field] = None
        except (TypeError, ValueError):
            self._attr_dict[field] = None

    def format_integer_value(self, field):
        value = self._attr_dict[field]
        self._attr_dict[field] = int(value) if value else None

    def format_float_value(self, field, integer_part_size):
        value = self._attr_dict[field]
        try:
            self._attr_dict[field] = float(
                value[0:0 + integer_part_size] + '.' + value[0 + integer_part_size:len(value)]) if value else None
        except (TypeError, ValueError):
            self._attr_dict[field] = None

    def format_time_value(self, field):
        value = self._attr_dict[field]
        try:
            if int(value) != 0:
                self._attr_dict[field] = datetime.datetime.strptime(value, '%H%M%S').time() if value else None
            else:
                self._attr_dict[field] = None
        except (TypeError, ValueError):
            self._attr_dict[field] = None

    def extract_value(self, starts, size):
        self.FIELD_VALUES.append(self.get_value(starts, size))

    def get_value(self, starts, size):
        value = self._record[starts:starts + size].strip()
        return value if value else None

    def __str__(self):
        return str(self._attr_dict)

    def __repr__(self):
        return self