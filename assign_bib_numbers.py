import sys
import csv

filepath = sys.argv[1]
out_filepath = filepath.replace(".csv", "-with-bib-numbers.csv")

with open(filepath, newline='', encoding='utf-8-sig') as csvin:
    # BikeReg exports , delimited with "" quotecars
    reader = csv.reader(csvin.readlines(), delimiter=',', quotechar='"')

with open(out_filepath, 'w', newline='', encoding='utf-8-sig') as csvout:
    writer = csv.writer(csvout, dialect='excel')
    for i, row in enumerate(reader):
        new_row = row
        if i > 0:
            new_row[0] = i
        writer.writerow(new_row)
