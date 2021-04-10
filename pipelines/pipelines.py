import os
import numpy as np

from utils import bikereg_utils as breg_utils
from utils import webscorer_utils as webscr_utils


def __data_dir(filepath, is_in_dir=True):
    # gets the input or output directory
    in_or_out_dir = 'in' if is_in_dir else 'out'
    return os.path.dirname(filepath) \
               .replace('/in', '') \
               .replace('/out', '') + \
           '/' + in_or_out_dir + '/' + \
           os.path.splitext(
               os.path.basename(filepath)
           )[0]


def in_dir(filepath):
    # convenience method for getting the input directory
    return __data_dir(filepath, True)


def out_dir(filepath):
    # convenience method for getting the output directory
    return __data_dir(filepath, False)


def dedup_bikreg_category_merch_column(bikereg_results_path, total_racers):
    #
    bikereg_results_df = breg_utils.read_csv_with_dtypes(bikereg_results_path)

    MERCH_PREFIXES = [
        'T shirt',
        'Trail Maintenance Donations',
        'BROC Membership',
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
        breg_utils.CAT_AND_MERCH: breg_utils.CATEGORY_ENTERED
    })

    # this utility is for results only so we don't want to
    # preserve the files with merchandise on them
    no_merch_df.to_csv(
        out_dir(bikereg_results_path) + '-deduped.csv',
        index=False
    )


def bib_numbers_path(filepath):
    return out_dir(filepath) + '-with-bib-numbers.csv'


def assign_bib_numbers(bikereg_path, sequence_start):
    registrants = breg_utils.read_csv_with_dtypes(bikereg_path)
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
    pre_reg_df = breg_utils.read_csv_with_dtypes(pre_reg_bib_nums_path)
    walk_up_df = breg_utils.read_csv_with_dtypes(walk_up_path)
    join_cols = list(pre_reg_df.columns.values)
    join_cols.remove('Bib')
    joined_df = pre_reg_df.merge(
        walk_up_df,
        on=join_cols,
        how='right'
    )
    joined_df.rename(columns={'Bib_x': 'Bib'}, inplace=True)
    joined_df.drop(columns='Bib_y', inplace=True)
    joined_df.to_csv(
        bikereg_join_path(pre_reg_bib_nums_path),
        index=False
    )


def webscorer_bikereg_join_path(filepath):
    return out_dir(filepath) + '-with-times.csv'


def join_webscorer_and_bikereg(
        webscorer_path,
        bikereg_path,
        staggered_time_marker_bibs,
        strict_matching=True):
    webscorer_df = webscr_utils.read_csv_with_dtypes(webscorer_path)
    webscorer_df.drop(
        columns=['Pl', 'Name'],
        inplace=True
    )
    webscorer_df.dropna(
        how='all',
        axis='columns',
        inplace=True
    )
    no_bib_numbers_df = webscorer_df[
        webscorer_df.apply(
            lambda df: df['Bib'] is np.NaN,
            axis=1
        )
    ]
    num_rows_without_bib = no_bib_numbers_df.shape[0]
    try:
        assert not num_rows_without_bib > 0
    except AssertionError as ass_err:
        ass_err.args += (num_rows_without_bib, 'rows have no bib numbers!')
        raise

    bikereg_df = breg_utils.read_csv_with_dtypes(bikereg_path)
    bikereg_df['Time'] = np.nan

    # add marker bibs to bikereg dataframe
    for marker_bib in staggered_time_marker_bibs:
        bikereg_df = bikereg_df.append(
            {
                'Bib': int(marker_bib)
            },
            ignore_index=True
        )

    for idx, webscorer_row in webscorer_df.iterrows():
        webscorer_bib_num = int(webscorer_row['Bib'])
        bikereg_row = bikereg_df.loc[bikereg_df['Bib'] == webscorer_bib_num]

        try:
            assert not bikereg_row.empty
        except AssertionError as ass_err:
            ass_err.args += ('No webscorer row found for bikereg df Bib: ', webscorer_row['Bib'])
            if strict_matching:
                raise

        if bikereg_row.empty:
            continue

        if webscorer_row['Time'] is not None:
            bikereg_df.loc[bikereg_df['Bib'] == webscorer_bib_num, 'Time'] = webscorer_row['Time']

    bikereg_df.to_csv(
        webscorer_bikereg_join_path(bikereg_path),
        index=False
    )


def time_transform_path(filepath):
    return out_dir(filepath) + '-time-adjusted.csv'
