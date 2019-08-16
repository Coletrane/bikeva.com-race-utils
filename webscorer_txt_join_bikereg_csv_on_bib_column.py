import sys
import pandas as pd

webscorer_path = sys.argv[1]
bikereg_path = sys.argv[2]
out_filepath = bikereg_path.replace(".csv", "with-times.csv")

webscorer_df = pd.read_csv(webscorer_path, delimiter='\t', header=0)
webscorer_df.drop(columns=['Place', 'Name'], inplace=True)
webscorer_df.dropna(how='all', axis='columns', inplace=True)

bikereg_df = pd.read_csv(bikereg_path, header=0)
bikereg_df.dropna(how='all', axis='columns', inplace=True)
# with_times_csv = bikereg_csv.merge(webscorer_csv, left_on='Bib')
print(webscorer_df)
print(bikereg_df)