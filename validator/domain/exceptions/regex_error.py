__author__ = 'Borja'


class RegexError(Exception):
    def __init__(self, field, regex, value):
        self.field = field
        self.regex = regex
        self.value = value

    def __str__(self):
        return 'REGEX ERROR: Record field {} does not validate value {} with expression given {}'.format(
                    self.field, self.value, self.regex)
