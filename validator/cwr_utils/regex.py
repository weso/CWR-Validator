__author__ = 'Borja'


def get_alpha_regex(size, optional=False):
    regex = '([A-Z]{%d})' % size
    return '({0}|{1})'.format(regex, get_optional_regex(size)) if optional else regex


def get_alphanumeric_regex(size, optional=False):
    regex = '([0-9A-Z]{%d})' % size
    return '({0}|{1})'.format(regex, get_optional_regex(size)) if optional else regex


def get_ascii_regex(size, optional=False):
    regex = '([ -~]{%d})' % size
    return '({0}|{1})'.format(regex, get_optional_regex(size)) if optional else regex


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

    regex += '|' + get_optional_regex(size) + ')' if optional else ')'
    return regex


def get_flag_regex(optional=False):
    regex = '([YNU])'
    return '({0}|{1})'.format(regex, get_optional_regex(1)) if optional else regex


def get_non_roman_regex(size, optional=False):
    regex = '(.{%d})' % size
    return '({0}|{1})'.format(regex, get_optional_regex(size)) if optional else regex


def get_numeric_regex(size, optional=False):
    regex = '(\d{%d})' % size
    return '({0}|{1})'.format(regex, get_optional_regex(size)) if optional else regex


def get_time_regex(optional=False):
    return get_numeric_regex(6, optional)


def get_optional_regex(size):
    return '( {%d})' % size