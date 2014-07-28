import os
from validator.domain.exceptions.regex_error import RegexError
from validator.validator import Validator
from uploads import __data__
__author__ = 'Borja'


def main():
    file_validator = Validator()
    print 'Validating file {}'.format(os.path.join(__data__.path(), 'CW1328EMI_059.V21'))

    try:
        file_validator.run(os.path.join(__data__.path(), 'CW1328EMI_059.V21'))

        with open('log', 'w') as f:
            for error in file_validator.document.errors.values():
                f.write(error)

    except RegexError as error:
        print error

if __name__ == '__main__':
    main()