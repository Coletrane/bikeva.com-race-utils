import datetime

import numpy as np

from pipelines import pipelines
from utils import bikereg_utils as breg_utils
from utils import time_utils
from utils import race_utils_common as race_utils

XXC_CATEGORIES = [
    'XXC Men',
    'XXC Women',
    'XXC Singlespeed',
    'XXC Master 45+',
    'XXC Master 55+',
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
    'Elementary 6th Grade and younger',
    'Junior Varsity 7-10th Grade',
    'Varsity High School Grade 11-12 (open)',
    'Class 1 E bike Open'
]


def time_transform(results_path, output_filename = None):
    results_df = breg_utils.read_csv_with_dtypes(results_path)
    results_df = time_utils.add_hours_digit(results_df)

    marker_bib_time = time_utils.row_time_to_secs(
        results_df.loc[results_df['Bib'] == race_utils.XC_START_MARKER_BIB_NUMBER].squeeze()
    )

    for idx, row in results_df.iterrows():
        if race_utils.is_xc(row, XC_CATEGORIES) and \
                row['Bib'] != race_utils.XC_START_MARKER_BIB_NUMBER and \
                row['Time'] is not np.nan and \
                row['Time'] != 'DNF':
            row_secs = time_utils.row_time_to_secs(row)
            results_df.loc[idx, 'Time'] = str(
                datetime.timedelta(
                    seconds=(row_secs - marker_bib_time)
                )
            )
            results_df.drop(
                results_df.loc[results_df['Bib'] == race_utils.XC_START_MARKER_BIB_NUMBER].index,
                inplace=True
            )

    if output_filename is None:
        output_filename = pipelines.time_transform_path(results_path),
    results_df.to_csv(
        output_filename,
        index=False
    )
