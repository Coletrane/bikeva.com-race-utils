import datetime

import numpy as np

from pipelines import pipelines
from utils import bikereg_utils as breg_utils
from utils import time_utils

XC_STAGGER = 'XC_STAGGER'
YOUTH_STAGGER = 'YOUTH_STAGGER'

# Since both races are running off of one clock, and the XC might not start EXACTLY at the
# time it is scheduled, I mark the time they start with an out of bounds bib number
MARKER_BIBS = {
    XC_STAGGER: 1111,
    YOUTH_STAGGER: 2222
}

XXC_CATEGORIES = [
    'XXC Men',
    'XXC Women',
    'XXC Singlespeed',
    'XXC Master 45+',
    'XXC Master 55+',
]

YOUTH_CATEGORIES = [
    'Elementary 6th Grade and younger',
    'Junior Varsity 7-10th Grade',
    'Varsity High School Grade 11-12 (open)'
]

XC_CATEGORIES = [
    'Expert Men (open)',
    'Master Expert Men 35+',
    'Expert Women (open)',
    'Sport Men 19-34',
    'Master Sport Men 35-44',
    'Master Men 45 - 54',
    'Master Men 55+',
    'Master Sport Women 35+',
    'Sport Women 19-34',
    'Beginner Men (open)',
    'Beginner Women (open)',
    'Singlespeed',
    'Class 1 E bike Open'
]


def is_xxc(row):
    return row['Category Entered'] in XXC_CATEGORIES


def is_youth(row):
    return row['Category Entered'] in YOUTH_CATEGORIES


def is_xc(row):
    return row['Category Entered'] in XC_CATEGORIES


def get_stagger_bib_num(row):
    if is_xxc(row):
        return

    if is_youth(row):
        return MARKER_BIBS[YOUTH_STAGGER]
    if is_xc(row):
        return MARKER_BIBS[XC_STAGGER]


def get_marker_bib_time(df, stagger_bib_num):
    marker_bib_row = df.loc[df['Bib'] == stagger_bib_num].squeeze()
    return time_utils.row_time_to_secs(marker_bib_row)


def time_transform(results_path, output_filename=None):
    results_df = breg_utils.read_csv_with_dtypes(results_path)
    results_df = time_utils.add_hours_digit(results_df)

    for idx, row in results_df.iterrows():
        # only transform the time for youth and xc times, throw out nan or 'DNF' times, don't do anything to the
        # marker bib numbers
        if is_xxc(row) or \
                row['Time'] is np.nan or \
                row['Time'] == 'DNF' or \
                row['Bib'] in MARKER_BIBS.items():
            continue

        stagger_bib_num = get_stagger_bib_num(row)
        if stagger_bib_num is None:
            continue
        marker_bib_time = get_marker_bib_time(results_df, stagger_bib_num)

        if marker_bib_time is not None:
            row_secs = time_utils.row_time_to_secs(row)
            row_secs_adjusted = row_secs - marker_bib_time
            row_date_adjusted = datetime.timedelta(seconds=row_secs_adjusted)
            results_df.loc[idx, 'Time'] = str(row_date_adjusted)

    # delete the marker bib times from the dataframe we'll output
    for key in MARKER_BIBS.keys():
        marker_bib_num = MARKER_BIBS[key]
        results_df.drop(
            results_df.loc[results_df['Bib'] == marker_bib_num].index,
            inplace=True
        )

    if output_filename is None:
        output_filename = pipelines.time_transform_path(results_path),
    results_df.to_csv(
        output_filename,
        index=False
    )
