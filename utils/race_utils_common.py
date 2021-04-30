import pandas as pd

from utils import bikereg_utils as breg_utils


def race_discipline(row):
    cat = row[breg_utils.CATEGORY_ENTERED]
    if cat.startswith('Marathon/XXC'):
        return breg_utils.DISCIPLINES['xcm']
    elif cat.startswith('XC'):
        return breg_utils.DISCIPLINES['xc']


def assign_bib_numbers_by_first_and_last_name(source_filepath, dest_filepath):
    source_df = pd.read_csv(source_filepath, header=0)
    dest_df = pd.read_csv(dest_filepath, header=0)

    for idx, row in source_df.iterrows():
        first_name = row['FIRST']
        last_name = row['LAST']

        dest_row_idx = dest_df.index[
            (dest_df['First Name'] == first_name) &
            (dest_df['Last Name'] == last_name)].values.item()
        dest_df.loc[dest_row_idx, 'Bib'] = row['NUMBER']

    output_filepath = dest_filepath.replace('.csv', '-joined-all.csv')
    dest_df.to_csv(output_filepath, index=False)


