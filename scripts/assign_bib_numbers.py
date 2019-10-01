import sys

import pandas as pd

filepath = sys.argv[1]
out_filepath = filepath.replace(".csv", "-with-bib-numbers.csv")

registrants = pd.read_csv(filepath)
registrants['Bib'] = range(1, 1 + len(registrants))
registrants.to_csv(
    out_filepath,
    index=False
)
