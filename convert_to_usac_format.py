import os
import sys

import pandas as pd

final_results_path = sys.argv[1]
usac_results_path = os.path.dirname(final_results_path) + '/' + \
                    os.path.basename(final_results_path) + \
                    '-usac-format.csv'
category_entered = 'Category Entered'

race_discipline = sys.argv[2]


def get_category_gender(row):
    cat = row[category_entered]
    cat_gender = None
    if cat.conttains('Women'):
        cat_gender = 'Women'
    elif cat.contains('Men'):
        cat_gender = 'Men'
    try:
        assert not cat_gender is None
    except AssertionError as ass_err:
        ass_err.args += (
            'No gender can be extracted from Category: ',
            cat
        )
        raise


final_results_df = pd.read_csv(final_results_path)
# todo: category and classes split
usac_results_df = pd.DataFrame({
    'Race Date': final_results_df['Category Date'],
    'Race Discipline': race_discipline,
    'Race Category': final_results_df[category_entered],
    'Race Gender': final_results_df.apply(get_category_gender, axis='columns'),
    'Race Class': [],
    'Race Age Group': [],
    'Rider License #': final_results_df['USAC License'],
    'Rider First Name': final_results_df['First Name'],
    'Rider Last Name': final_results_df['Last Name'],
    'Rider Place': final_results_df['Position']
})
