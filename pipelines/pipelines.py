import os

import pandas as pd

from utils import bikereg_utils as breg_utils


def out_dir(filepath):
    return os.path.dirname(filepath) \
               .replace('/in', '') \
               .replace('/out', '') + \
           '/out/' + \
           os.path.splitext(
               os.path.basename(filepath)
           )[0]


def no_merch_path(filepath):
    return out_dir(filepath) + '-no-merch.csv'


def dedup_bikreg_category_merch_column(bikereg_results_path, total_racers):
    bikereg_results_df = pd.read_csv(bikereg_results_path)

    MERCH_PREFIXES = [
        'T shirt',
        'Trail Maintenance Donations Welcomed',
        'License',
        'Ultraclub Tech T'
    ]

    def is_not_merch(row):
        cat = row[breg_utils.CAT_AND_MERCH]
        is_merch = False
        for prefix in MERCH_PREFIXES:
            if is_merch:
                break
            is_merch = cat.startswith(prefix)

        return not is_merch

    no_merch_df = bikereg_results_df.apply(
        is_not_merch,
        axis='columns'
    )
    no_merch_df = bikereg_results_df[no_merch_df]

    try:
        assert no_merch_df.shape[0] == total_racers
    except AssertionError as ass_err:
        ass_err.args += (
            'DataFrame rows: ',
            no_merch_df.shape[0],
            'has less than total racers arg: ',
            total_racers
        )
        raise

    no_merch_df = no_merch_df.rename(columns={
        breg_utils.CAT_AND_MERCH: 'Category Entered'
    })

    no_merch_df.to_csv(
        no_merch_path(bikereg_results_path),
        index=False
    )


def bib_numbers_path(filepath):
    return out_dir(filepath) + '-with-bib-numbers.csv'


def assign_bib_numbers(bikereg_path, sequence_start):
    registrants = pd.read_csv(bikereg_path)
    registrants['Bib'] = range(
        sequence_start,
        sequence_start + len(registrants)
    )
    registrants.to_csv(
        bib_numbers_path(bikereg_path),
        index=False
    )


def bikereg_join_path(filepath):
    return out_dir(filepath) + '-all-reg.csv'


def join_bikereg_csvs(pre_reg_bib_nums_path, walk_up_path):
    pre_reg_df = pd.read_csv(pre_reg_bib_nums_path)
    walk_up_df = pd.read_csv(walk_up_path)
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
        bikereg_join_path(pre_reg_bib_nums_path),
        index=False
    )


def webscorer_bikereg_join_path(filepath):
    return out_dir(filepath) + 'with-times.csv'


def join_webscorer_and_bikereg(webscorer_path, bikereg_path):
    webscorer_df = pd.read_csv(webscorer_path, delimiter='\t', header=0)
    webscorer_df.drop(
        columns=['Place', 'Name'],
        inplace=True
    )
    webscorer_df.dropna(
        how='all',
        axis='columns',
        inplace=True
    )
    no_bib_numbers_df = webscorer_df[
        webscorer_df.apply(
            lambda df: df['Bib'] == 0,
            axis=1
        )
    ]
    num_rows_without_bib = no_bib_numbers_df.shape[0]
    try:
        assert not num_rows_without_bib > 0
    except AssertionError as ass_err:
        ass_err.args += (num_rows_without_bib, 'rows have no bib numbers!')
        raise

    bikereg_df = pd.read_csv(
        bikereg_path,
        header=0
    )
    bikereg_df.dropna(
        how='all',
        axis='columns',
        inplace=True
    )

    with_times_df = bikereg_df.merge(
        webscorer_df,
        how='left',
        on='Bib'
    )
    with_times_df.to_csv(
        webscorer_bikereg_join_path(bikereg_path),
        index=False
    )


def add_hours_digit(dataframe, rowname):
    """
     Convert times to HH:MM:SS.S format with 0
    :param dataframe: dataframe to operate on
    :param rowname: name of the row with times
    :return the new dataframe
    """
    for row in dataframe[rowname].itterows():
        times = row.split(':')
        if len(times) == 2:
            row = f'0:{row}'

    return dataframe


def row_time_to_secs(row):
    hrs, mins, secs = row['Time'].split(':')

    hrs_secs = hrs * 60 * 60
    mins_secs = mins * 60

    return float(hrs_secs + mins_secs + secs)


def time_transform_path(filepath):
    return out_dir(filepath) + 'time-adjusted.csv'


def time_transform(results_path, staggered_time_marker_bibs):
    results_df = pd.read_csv(results_path, delimiter='\t', header=0)
    results_df = add_hours_digit(
        results_df,
        'Time'
    )
    # TODO: make this look at category for Middle Mountain Momma
    marker_bib_time = None
    for row in results_df.iterrows():
        if row['Bib'] in staggered_time_marker_bibs:
            marker_bib_time = row_time_to_secs(row)

        if marker_bib_time is not None:
            row_secs = row_time_to_secs(row)
            row['Time'] = str(row_secs - marker_bib_time)

    results_df.to_csv(
        time_transform_path(results_path),
        index=False
    )
