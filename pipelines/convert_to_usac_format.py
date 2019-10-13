import os
import sys

import pandas as pd

from utils import bikereg_utils as breg_utils
from utils import creature_utils as creature

final_results_path = sys.argv[1]
usac_results_path = os.path.splitext(final_results_path)[0] +\
                    '-usac-format.csv'

final_results_df = pd.read_csv(final_results_path)

usac_results_df = pd.DataFrame({
    'Race Date':
        final_results_df['Category Date'],
    'Race Discipline':
        final_results_df.apply(creature.race_discipline, axis='columns'),
    'Race Category':
        final_results_df.apply(breg_utils.get_race_cat, axis='columns'),
    'Race Gender':
        final_results_df.apply(breg_utils.get_category_gender, axis='columns'),
    'Race Class':
        final_results_df.apply(
            lambda row: breg_utils.get_race_class(row, creature.XC_DISCIPLINES),
            axis='columns'
        ),
    'Race Age Group':
        final_results_df.apply(
            lambda row: breg_utils.get_race_age_group(row, creature.DISCIPLINE_AGE_GROUPS),
            axis='columns'
        ),
    'Rider License #':
        final_results_df['USAC License'],
    'Rider First Name':
        final_results_df['First Name'],
    'Rider Last Name':
        final_results_df['Last Name'],
    'Rider Place':
        [None] * len(final_results_df.index)
})

usac_results_df.to_csv(
    usac_results_path,
    index=False
)
