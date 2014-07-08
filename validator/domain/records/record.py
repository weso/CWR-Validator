__author__ = 'Borja'
import abc
import datetime
import re


class Record(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, record, regex):
        print record
        matcher = re.compile(regex)
        if matcher.match(record):
            self._record = record
            self._build_record(record)
        else:
            raise ValueError('Given record: \n[%s] \ndoes not match required format \n[%s]' % (record, regex))

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

    def get_date_value(self, starts, size):
        value = self.get_value(starts, size)
        try:
            return datetime.datetime.strptime(value, '%Y%m%d').date() if value else None
        except ValueError:
            return None

    def get_integer_value(self, starts, size):
        value = self.get_value(starts, size)
        return int(value) if value else None

    def get_float_value(self, starts, size, integer_part_size):
        value = self.get_value(starts, size)
        try:
            return float(
                value[0:0 + integer_part_size] + '.' + value[0 + integer_part_size:size]) if value else None
        except ValueError:
            return None

    def get_time_value(self, starts, size):
        value = self.get_value(starts, size)
        try:
            return datetime.datetime.strptime(value, '%H%M%S').time() if value else None
        except ValueError:
            return None

    def get_value(self, starts, size):
        value = self._record[starts:starts + size].strip()
        return value if value else None