__author__ = 'Borja'


class Regex(object):

    def __init__(self, regex=None, size=None):
        self._regex = regex.encode('utf-8')
        self._size = size

    @property
    def regex(self):
        return self._regex

    @property
    def size(self):
        return self._size

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Regex(self._regex + other._regex, self._size + other._size)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    def __str__(self):
        return self._regex


def get_alpha_regex(size, optional=False):
    if optional:
        regex = '({0}|{1})'.format('([A-Z]{%d})' % size, str(get_optional_regex(size)))
    else:
        regex = '([A-Z]{%d})' % size

    return Regex(regex, size)


def get_alphanumeric_regex(size, optional=False):
    if optional:
        regex = '({0}|{1})'.format('([0-9A-Z]{%d})' % size, str(get_optional_regex(size)))
    else:
        regex = '([0-9A-Z]{%d})' % size

    return Regex(regex, size)


def get_ascii_regex(size, optional=False):
    if optional:
        regex = '({0}|{1})'.format('([ -~]{%d})' % size, str(get_optional_regex(size)))
    else:
        regex = '([ -~]{%d})' % size

    return Regex(regex, size)


def get_boolean_regex(optional=False):
    if optional:
        regex = '({0}|{1})'.format('([YN])', str(get_optional_regex(1)))
    else:
        regex = '([YN])'

    return Regex(regex, 1)


def get_date_regex(optional=False):
    return get_numeric_regex(8, optional)


def get_defined_values_regex(size, optional=False, *args):
    first = True
    regex = '('
    for value in args:
        if first:
            regex += ('(' + value + ')')
            first = False
        else:
            regex += ('|(' + value + ')')

    regex += '|' + str(get_optional_regex(size)) + ')' if optional else ')'

    return Regex(regex, size)


def get_flag_regex(optional=False):
    if optional:
        regex = '({0}|{1})'.format('([YNU])', str(get_optional_regex(1)))
    else:
        regex = '([YNU])'

    return Regex(regex, 1)


def get_non_roman_regex(size, optional=False):
    if optional:
        regex = '({0}|{1})'.format('(.{%d})' % size, str(get_optional_regex(size)))
    else:
        regex = '(.{%d})' % size

    return Regex(regex, size)


def get_numeric_regex(size, optional=False):
    if optional:
        regex = '({0}|{1})'.format('(\d{%d})' % size, str(get_optional_regex(size)))
    else:
        regex = '(\d{%d})' % size

    return Regex(regex, size)


def get_time_regex(optional=False):
    return get_numeric_regex(6, optional)


def get_optional_regex(size):
    return Regex('( {%d})' % size, size)