import os
import sys

import pandas as pd

bikereg_results_path = sys.argv[1]
total_racers = int(sys.argv[2])
no_merch_path = os.path.splitext(bikereg_results_path)[0] + \
                '-no-merch.csv'

bikereg_results_df = pd.read_csv(bikereg_results_path)


def is_not_merch(row):
    cat = row['Category Entered / Merchandise Ordered']
    is_merch = cat.startswith('T shirt') or \
               cat.startswith('Trail Maintenance Donations Welcomed')
    return not is_merch


no_merch_df = bikereg_results_df.apply(
    is_not_merch,
    axis='columns'
)
no_merch_df = bikereg_results_df[no_merch_df]

try:
    assert no_merch_df.shape[0] == total_racers
except AssertionError as ass_err:
    ass_err.args += (total_racers, 'no_merch_df has less than total_racers!')
    raise

no_merch_df.to_csv(
    no_merch_path,
    index=False
)
