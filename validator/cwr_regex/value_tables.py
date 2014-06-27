__author__ = 'Borja'
import csv
import xlrd


AGREEMENT_TYPE_VALUES = {'OG', 'OS', 'PG', 'PS'}


def _load_currency_values():
    codes = []
    workbook = xlrd.open_workbook('../files/currency_values.xls')
    worksheet = workbook.sheet_by_name('Active')

    for curr_row in range(4, 282):
        codes.append(worksheet.cell_value(curr_row, 2))

    codes = sorted(list(set(codes)))  # Remove duplicates
    codes.remove('')  # Remove empty values

    return codes

COMPOSITE_TYPE = ['COS', 'MED', 'POT', 'UCO']

CURRENCY_VALUES = _load_currency_values()

DISTRIBUTION_CATEGORY_TABLE = ['JAZ', 'POP', 'SER', 'UNC']

IPA_TYPES = ['AC', 'AS']


def _load_language_code_values():
    with open('../files/language_codes.csv') as csv_file:
        language_codes = csv.reader(csv_file)

    return language_codes

LANGUAGE_CODES = _load_language_code_values()

LYRIC_ADAPTATION = ['NEW', 'MOD', 'NON', 'ORI', 'REP', 'ADL', 'UNS', 'TRA']

MUSIC_ARRANGEMENT_TYPES = ['NEW', 'ARR', 'ADM', 'UNS', 'ORI']

SENDER_VALUES = {'PB', 'SO', 'AA', 'WR'}


def _load_societies_codes():
    codes = []
    workbook = xlrd.open_workbook('../files/SG12-1020_CISAC_Societies_Codes_2014-06-09_EN.xls')
    worksheet = workbook.sheet_by_name('CISAC Societies Codes listing')

    for curr_row in range(1, worksheet.nrows):
        codes.append(int(worksheet.cell_value(curr_row, 0)))

    return codes

SOCIETY_CODES = _load_societies_codes()


def _load_tis_codes():
    codes = []
    workbook = xlrd.open_workbook('../files/TIS09-1540a_Territories_2009-08-27_EN.xls')
    worksheet = workbook.sheet_by_name('en')

    for curr_row in range(1, worksheet.nrows):
        codes.append(int(worksheet.cell_value(curr_row, 0)))

    return codes

TEXT_MUSIC_TABLE = ['MUS', 'MTX', 'TXT']

TIS_CODES = _load_tis_codes()

TRANSACTION_VALUES = {'AGR', 'NWR', 'REV'}


def _load_work_types():
    with open('../files/cwr_work_types.csv') as csv_file:
        work_types = csv.reader(csv_file)

    return work_types

WORK_TYPES = _load_work_types()


