import pandas as pd

bib_df = pd.read_csv(
    '../../data/creature-2019/out/bikereg-with-bib-numbers-one-off.csv',
    header=0
)
for idx, row in  bib_df.iterrows():
    bib_df.loc[idx, 'Bib'] = row['Bib'] + 1

bib_df.to_csv('../../data/creature-2019/out/bikereg-with-bib-numbers.csv', index=False)