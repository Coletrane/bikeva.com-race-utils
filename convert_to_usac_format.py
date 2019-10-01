import os
import sys

import pandas as pd

final_results_path = sys.argv[1]
usac_results_path = os.path.dirname(final_results_path) + '/' + \
                    os.path.basename(final_results_path) + \
                    '-usac-format.csv'

race_discipline = sys.argv[2]

final_results_df = pd.read_csv(final_results_path)
usac_results_df = pd.DataFrame({
    'Race Date': final_results_df['Category Date'],
    'Race Discipline': race_discipline,
    'Race Category': final_results_df['Category Entered'],
    'Race Gender',
    'Race Class',
    'Race Age Group',
    'Rider License #',
    'Rider First Name',
    'Rider Last Name',
    'Rider Place'
})

