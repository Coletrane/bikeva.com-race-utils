import datetime

import numpy as np

from pipelines import pipelines
from utils import bikereg_utils as breg_utils
from utils import time_utils

MARATHON_XXC = 'Marathon/XXC'
XC = 'XC'
ENDURO = 'enduro'

XC_DISCIPLINES = [
    MARATHON_XXC,
    XC
]

XC_CATEGORIES = [
    'XC Beginner Men Cat 3',
    'XC Beginner Women Cat 3',
    'XC Sport Men Cat 2 19+',
    'XC Sport Women Cat 2 19+',
    'XC JR Varsity 7-10th Grade Cat 2/3',
    'XC Elementary 1-6th Grade Cat 2/3',
    'XC Varsity 11-12th Grade Cat 2/3',
    'XC Expert Men Pro/1',
    'XC Expert Women Pro/1',
    'XC Master Men 35+ Cat 2/3',
    'XC Master Men 45+ Cat 2/3',
    'XC Master Women 35+ Cat 2/3'
]

DISCIPLINE_AGE_GROUPS = {
    MARATHON_XXC: [
        '45+',
        '55+'
    ],
    XC: [
        '19+',
        '1-6th Grade',
        '7-10th Grade',
        '11-12th Grade',
        '35+',
        '45+',
        '55+'
    ],
    ENDURO: [
        '19-99',
        '9-14',
        '15-18',
        '9-99',
        '50-99',
        '19-21',
        '40-49'
    ]
}

# Since both races are running off of one clock, and the XC might not start EXACTLY at the
# time it is scheduled, I mark the time they start with an out of bounds bib number
XC_START_MARKER_BIB_NUMBER = 66666


def race_discipline(row):
    cat = row[breg_utils.CATEGORY_ENTERED]
    if cat.startswith(MARATHON_XXC):
        return breg_utils.DISCIPLINES['xcm']
    elif cat.startswith('XC'):
        return breg_utils.DISCIPLINES['xc']


def is_xc(row):
    return row[breg_utils.CATEGORY_ENTERED] in XC_CATEGORIES


def time_transform(results_path):
    results_df = breg_utils.read_csv_with_dtypes(results_path)
    results_df = time_utils.add_hours_digit(results_df)

    marker_bib_time = time_utils.row_time_to_secs(
        results_df.loc[results_df['Bib'] == XC_START_MARKER_BIB_NUMBER].squeeze()
    )

    for idx, row in results_df.iterrows():
        if is_xc(row) and \
                row['Bib'] != XC_START_MARKER_BIB_NUMBER and \
                row['Time'] is not np.nan:
            row_secs = time_utils.row_time_to_secs(row)
            results_df.loc[idx, 'Time'] = str(
                datetime.timedelta(
                    seconds=(row_secs - marker_bib_time)
                )
            )
            results_df.drop(
                results_df.loc[results_df['Bib'] == XC_START_MARKER_BIB_NUMBER].index,
                inplace=True
            )

    results_df.to_csv(
        pipelines.time_transform_path(results_path),
        index=False
    )
