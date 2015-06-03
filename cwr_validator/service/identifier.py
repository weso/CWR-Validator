# -*- encoding: utf-8 -*-

import logging
from abc import ABCMeta, abstractmethod
import uuid

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class IdentifierService(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def generate_id(self):
        raise NotImplementedError('The generate_id method must be implemented')


class UUIDIdentifierService(IdentifierService):
    _logger = logging.getLogger(__name__)

    def __init__(self):
        super(UUIDIdentifierService, self).__init__()

    def generate_id(self):
        return uuid.uuid4()
