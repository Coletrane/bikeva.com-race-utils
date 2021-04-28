import datetime

import numpy as np
import pandas as pd

from pipelines import pipelines
from utils import bikereg_utils as breg_utils
from utils import time_utils

EBIKE = 'EBIKE'
G1 = 'G1'
G2 = 'G2'
G3 = 'G3'
G4 = 'G4'
G5 = 'G5'
G6 = 'G6'
G7 = 'G7'

# Since both races are running off of one clock, and the XC might not start EXACTLY at the
# time it is scheduled, I mark the time they start with an out of bounds bib number
MARKER_BIBS = {
    EBIKE: 9999,
    G1: 1111,
    G2: 2222,
    G3: 3333,
    G4: 4444,
    G5: 5555,
    G6: 6666,
    G7: 7777
}


def get_group_marker_bibs():
    return filter(lambda key: key != EBIKE, MARKER_BIBS.keys())


XXC_CATEGORIES = [
    'XXC Men',
    'XXC Women',
    'XXC Singlespeed',
    'XXC Master 45+',
    'XXC Master 55+',
]

GROUP_CATEGORIES = [
    [''],  # indexed by 1 so it makes sense with the spreadsheet ("Group 1", "Group 2", ect.)
    [
        'Expert Men (open)'
    ],
    [
        'Master Expert Men 35+',
        'Singlespeed',
        'Varsity High School Grade 11-12 (open)'
    ],
    [
        'Expert Women (open)'
    ],
    [
        'Master Sport Men 35-44',
        'Master Men 45 - 54',
        'Master Men 55+'
    ],
    [
        'Sport Men (open)'
    ],
    [
        'Master Sport Women 35+',
        'Sport Women (open)'
    ],
    [
        'Sport Men 19-34',
        'Junior Varsity 7-10th Grade',
        'Beginner Men (open)',
        'Beginner Women (open)',
        'Elementary 6th Grade and younger'
    ]
]

EBIKE_CATEGORY = 'Class 1 E-Bike (open)'


# doesn't work and getting frustrated with pandas weirdness
# def assign_bib_numbers_momma_2021(bikereg_path):
#     all_reg_df = breg_utils.read_csv_with_dtypes(bikereg_path)
#     non_xxc_df = all_reg_df[~all_reg_df['Category Entered'].isin(XXC_CATEGORIES)]
#     xxc_df = all_reg_df[all_reg_df['Category Entered'].isin(XXC_CATEGORIES)]
#
#     try:
#         assert not len(non_xxc_df) > 100
#     except AssertionError as ass_err:
#         ass_err.args += 'there are more than 100 non XXC racers! You need front plates'
#         raise
#
#     non_xxc_df.loc['Bib'] = range(
#         601,
#         601 + len(non_xxc_df)
#     )
#
#     xxc_df.loc['Bib'] = range(
#         700,
#         700 + len(xxc_df)
#     )
#
#     result_df = pd.concat([non_xxc_df, xxc_df])
#     result_df.to_csv(
#         pipelines.bib_numbers_path(bikereg_path),
#         index=False
#     )


def is_xxc(row):
    return row['Category Entered'] in XXC_CATEGORIES


def is_ebike(row):
    return row['Category Entered'] == EBIKE_CATEGORY


def is_group_category(row):
    return get_stagger_bib_group_number_string(row) is not None


def get_stagger_bib_group_number_string(row):
    for idx in range(len(GROUP_CATEGORIES)):
        category = row['Category Entered']
        group_list = GROUP_CATEGORIES[idx]
        if category not in group_list:
            continue

        return f"G{idx}"


def get_group_stagger_bib_number(row):
    stagger_bib_group = get_stagger_bib_group_number_string(row)
    return MARKER_BIBS[stagger_bib_group]


def get_stagger_bib_num(row):
    if is_xxc(row):
        return

    if is_ebike(row):
        return MARKER_BIBS[EBIKE]

    if is_group_category(row):
        return get_group_stagger_bib_number(row)


def get_marker_bib_time(df, stagger_bib_num):
    marker_bib_row = df.loc[df['Bib'] == stagger_bib_num].squeeze()
    return time_utils.row_time_to_secs(marker_bib_row)


def validate_categories(bikereg_path):
    bikereg_df = breg_utils.read_csv_with_dtypes(bikereg_path)
    for idx, row in bikereg_df.iterrows():
        try:
            assert is_xxc(row) or is_ebike(row) or is_group_category(row)
        except AssertionError as ass_err:
            category = row['Category Entered']
            ass_err.args += ('Category ', category,' not found!')
            raise


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
