import pandas as pd

from utils import time_tansform_utils as ttf_util
from utils import bikereg_utils as breg_utils

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

XC_TIME_DIFF = 3
XC_TIME_DIFF_SECS = float(60 * 60 * XC_TIME_DIFF)

def race_discipline(row):
    cat = row[breg_utils.CATEGORY_ENTERED]
    if cat.startswith(MARATHON_XXC):
        return breg_utils.DISCIPLINES['xcm']
    elif cat.startswith('XC'):
        return breg_utils.DISCIPLINES['xc']

def time_transform(results_path):
    results_df = pd.read_csv(results_path, delimiter='\t', header=0)
    results_df = ttf_util.add_hours_digit(
        results_df,
        'Time'
    )
    for row in results_df['Time'].iterrows():
        hrs, mins, secs = row.split(':')
        hrs_and_mins_secs = ttf_util.hrs_and_mins_to_secs(int(hrs), int(mins))
        total_row_secs = float(hrs_and_mins_secs) + float(secs)
        adjusted_secs = total_row_secs + XC_TIME_DIFF_SECS
        row = str(adjusted_secs)

    results_df.to_csv(
        results_path,
        index=False
    )
