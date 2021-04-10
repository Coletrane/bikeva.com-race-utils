import pandas as pd


def read_txt_with_dtypes(filepath):
    return pd.read_csv(
        filepath,
        delimiter='\t',
        header=0,
        dtype={
            'Place': str,
            'Bib': str,
            'Name': str,
            'Time': str
        }
    )


def read_csv_with_dtypes(filepath):
    return pd.read_csv(
        filepath,
        dtype={
            'Pl': str,
            'Bib': str,
            'Name': str,
            'Time': str
        }
    )
