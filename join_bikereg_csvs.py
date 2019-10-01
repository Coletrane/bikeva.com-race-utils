import os
import sys

import pandas as pd

pre_reg_with_bib_numbers_path = sys.argv[1]
with_walk_up_path = sys.argv[2]
out_filepath = os.path.dirname(pre_reg_with_bib_numbers_path) + '/' + \
               os.path.basename(pre_reg_with_bib_numbers_path) + \
               '-all-reg.csv'

pre_reg_df = pd.read_csv(pre_reg_with_bib_numbers_path)
walk_up_df = pd.read_csv(with_walk_up_path)
joined_df = pd.merge(
    pre_reg_df, walk_up_df,
    on=['First Name', 'Last Name', 'Category Entered/Merchandise Ordered'],
    how='right'
)
joined_df.drop(
    columns=['Bib_y'],
    inplace=True
)
joined_df.rename(
    columns={
        'Bib_x': 'Bib'
    },
    inplace=True
)
joined_df['Bib'] = joined_df['Bib'].astype('Int32')

joined_df.to_csv(
    out_filepath,
    index=False
)
