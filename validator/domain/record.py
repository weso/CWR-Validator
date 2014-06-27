__author__ = 'Borja'
import abc
import re


class Record(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, record, regex):
        print record
        matcher = re.compile(regex)
        if matcher.match(record):
            self._build_record(record)
        else:
            raise ValueError('Given record: \n[%s] \ndoes not match required format \n[%s]' % (record, regex))

    @abc.abstractmethod
    def _build_record(self, record):
        """ This method should by the record object related
            by reading the line in the CWR and validating the fields"""
        return