__author__ = 'Borja'


def enum(**enums):
    return type('Enum', (), enums)
