import sys
import pandas as pd
from time_transforms import time_tansform_utils as utils

xc_categories = [
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
xc_time_diff_hrs = 3
xc_time_diff_secs = float(60 * 60 * xc_time_diff_hrs)

results_path = sys.argv[1]

results_df = pd.read_csv(results_path, delimiter='\t', header=0)
results_df = utils.add_hours_digit(results_df, 'Time')
for index, row in results_df['Time'].iterrows():
    hrs, mins, secs = row.split(':')
    hrs_and_mins_secs = utils.hrs_and_mins_to_secs(int(hrs), int(mins))
    total_row_secs = float(hrs_and_mins_secs) + float(secs)
    adjusted_secs = total_row_secs + xc_time_diff_secs
    row = str(adjusted_secs)

results_df.to_csv(results_path)