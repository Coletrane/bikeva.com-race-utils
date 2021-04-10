from utils import bikereg_utils as breg_utils


def race_discipline(row):
    cat = row[breg_utils.CATEGORY_ENTERED]
    if cat.startswith('Marathon/XXC'):
        return breg_utils.DISCIPLINES['xcm']
    elif cat.startswith('XC'):
        return breg_utils.DISCIPLINES['xc']


