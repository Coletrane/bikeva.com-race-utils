import sys
import pandas as pd

webscorer_path = sys.argv[1]
bikereg_path = sys.argv[2]
out_filepath = bikereg_path.replace(".csv", "with-times.csv")

webscorer_df = pd.read_csv(webscorer_path, delimiter='\t', header=0)
webscorer_df.drop(columns=['Place', 'Name'], inplace=True)
webscorer_df.dropna(how='all', axis='columns', inplace=True)
no_bib_numbers_df = webscorer_df[webscorer_df.apply(lambda df: df['Bib'] == 0, axis=1)]
num_rows_without_bib = no_bib_numbers_df.shape[0]
try:
    assert not num_rows_without_bib > 0
except AssertionError as ass_err:
    ass_err.args += (num_rows_without_bib, 'rows have no bib numbers!')
    raise

bikereg_df = pd.read_csv(bikereg_path, header=0)
bikereg_df.dropna(how='all', axis='columns', inplace=True)

with_times_df = bikereg_df.merge(webscorer_df, how='left', on='Bib')
with_times_df.to_csv(out_filepath)
