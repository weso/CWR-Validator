# -*- encoding: utf-8 -*-
from __future__ import absolute_import
import csv
import os

import xlrd

from files import __data__


"""
Defines several CWR data types.
"""

__author__ = 'Borja Garrido Bear'
__license__ = 'MIT'
__version__ = '0.0.0'
__status__ = 'Development'

AGREEMENT_TYPE_VALUES = {'OG': None, 'OS': None, 'PG': None, 'PS': None}

COMPOSITE_TYPE = ['COS', 'MED', 'POT', 'UCO']


def _load_currency_values():
    codes = []
    workbook = xlrd.open_workbook(os.path.join(__data__.path(), os.path.basename('currency_values.xls')))
    worksheet = workbook.sheet_by_name('Active')

    for curr_row in range(4, 282):
        codes.append(worksheet.cell_value(curr_row, 2))

    codes = sorted(list(set(codes)))  # Remove duplicates
    if '' in codes:
        codes.remove('')  # Remove empty values

    return codes


CURRENCY_VALUES = _load_currency_values()

DISTRIBUTION_CATEGORY_TABLE = ['JAZ', 'POP', 'SER', 'UNC']

EXCERPT_TYPE = ['MOV', 'UEX']


def _load_instrument_codes():
    codes = []
    workbook = xlrd.open_workbook(os.path.join(__data__.path(), os.path.basename('CISAC-Instrument.xlsx')))
    worksheet = workbook.sheet_by_index(0)

    for curr_row in range(2, worksheet.nrows):
        codes.append(worksheet.cell_value(curr_row, 3))

    codes = sorted(list(set(codes)))  # Remove duplicates
    if '' in codes:
        codes.remove('')  # Remove empty values

    return codes


INSTRUMENT_CODES = _load_instrument_codes()


def _load_instrumentation_codes():
    codes = []
    workbook = xlrd.open_workbook(
        os.path.join(__data__.path(), os.path.basename('CISAC-Standard_instrumentation.xlsx')))
    worksheet = workbook.sheet_by_index(0)

    for curr_row in range(2, worksheet.nrows):
        codes.append(worksheet.cell_value(curr_row, 2))

    codes = sorted(list(set(codes)))  # Remove duplicates
    if '' in codes:
        codes.remove('')  # Remove empty values

    return codes


INSTRUMENTATION_CODES = _load_instrumentation_codes()

INTENDED_PURPOSES = ['COM', 'FIL', 'GEN', 'LIB', 'MUL', 'RAD', 'TEL', 'THR', 'VID']

IPA_TYPES = ['AC', 'AS']


def _load_language_code_values():
    language_codes = []
    with open(os.path.join(__data__.path(), os.path.basename('language_codes.csv'))) as csv_file:
        reader = csv.reader(csv_file)
        for csv_list in reader:
            for value in csv_list:
                language_codes.append(value)

    return language_codes


LANGUAGE_CODES = _load_language_code_values()

LYRIC_ADAPTATION = ['NEW', 'MOD', 'NON', 'ORI', 'REP', 'ADL', 'UNS', 'TRA']


def _load_media_types():
    media_types = []
    workbook = xlrd.open_workbook(os.path.join(__data__.path(), os.path.basename('BIEM-Media_types.xlsx')))
    worksheet = workbook.sheet_by_index(0)
    for curr_row in range(2, worksheet.nrows):
        media_types.append(worksheet.cell_value(curr_row, 4))

    media_types = sorted(list(set(media_types)))  # Remove duplicates
    if '' in media_types:
        media_types.remove('')  # Remove empty values

    return media_types


MEDIA_TYPES = _load_media_types()

MUSIC_ARRANGEMENT_TYPES = ['NEW', 'ARR', 'ADM', 'UNS', 'ORI']

PUBLISHER_TYPES = ['AM', 'AQ', 'E', 'ES', 'PA', 'SE']

RECORDING_FORMAT = ['A', 'V']

RECORDING_TECHNIQUE = ['A', 'D', 'U']

RIGHT_TYPES = ['ALL', 'MEC', 'PER', 'SYN']

SENDER_VALUES = {'PB': None, 'SO': None, 'AA': None, 'WR': None}


def _load_societies_codes():
    codes = []
    workbook = xlrd.open_workbook(
        os.path.join(__data__.path(), os.path.basename('SG12-1020_CISAC_Societies_Codes_2014-06-09_EN.xls')))
    worksheet = workbook.sheet_by_name('CISAC Societies Codes listing')

    for curr_row in range(1, worksheet.nrows):
        codes.append(int(worksheet.cell_value(curr_row, 0)))

    codes = sorted(list(set(codes)))  # Remove duplicates
    if '' in codes:
        codes.remove('')  # Remove empty values

    return codes


SOCIETY_CODES = _load_societies_codes()

SUBJECT_CODES = ['DL', 'SC', 'DW', 'IQ', 'RQ']


def _load_tis_codes():
    codes = []
    workbook = xlrd.open_workbook(
        os.path.join(__data__.path(), os.path.basename('TIS09-1540a_Territories_2009-08-27_EN.xls')))
    worksheet = workbook.sheet_by_name('en')

    for curr_row in range(1, worksheet.nrows):
        codes.append(int(worksheet.cell_value(curr_row, 0)))

    return codes


TEXT_MUSIC_TABLE = ['MUS', 'MTX', 'TXT']

TITLE_TYPES = ['AT', 'TE', 'FT', 'IT', 'OT', 'TT', 'PT', 'RT', 'ET', 'OL', 'AL']

TIS_CODES = _load_tis_codes()

TRANSACTION_VALUES = {'AGR': None, 'NWR': None, 'REV': None}

VERSION_TYPES = ['MOD', 'ORI']


def _load_work_types():
    work_types = []
    with open(os.path.join(__data__.path(), os.path.basename('cwr_work_types.csv'))) as csv_file:
        reader = csv.reader(csv_file)
        for csv_list in reader:
            for value in csv_list:
                work_types.append(value)

    return work_types


WORK_TYPES = _load_work_types()

WRITER_DESIGNATIONS = ['AD', 'AR', 'A', 'C', 'CA', 'SR', 'SA', 'TR', 'PA']

WRITER_POSITIONS = ['COW', 'EWT', 'VER']