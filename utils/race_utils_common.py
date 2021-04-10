from utils import bikereg_utils as breg_utils

# Since both races are running off of one clock, and the XC might not start EXACTLY at the
# time it is scheduled, I mark the time they start with an out of bounds bib number
XC_START_MARKER_BIB_NUMBER = 66666


def race_discipline(row):
    cat = row[breg_utils.CATEGORY_ENTERED]
    if cat.startswith('Marathon/XXC'):
        return breg_utils.DISCIPLINES['xcm']
    elif cat.startswith('XC'):
        return breg_utils.DISCIPLINES['xc']


def is_xc(row, xc_categories):
    return row[breg_utils.CATEGORY_ENTERED] in xc_categories
