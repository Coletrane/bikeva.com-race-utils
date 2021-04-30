# Run this file AFTER entering walk up registration into BikeReg and re-exporting it

from pipelines import pipelines
from utils import momma_utils as momma
from utils import race_utils_common as race_utils

# TODO: this is a test directory
DATA_PATH = '../../data/momma-2021'
BIKEREG_PATH = DATA_PATH + '/in/bikereg.csv'


# stuff to run always here such as class/def
def main():
    pass


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here

    # pipelines.dedup_bikreg_category_merch_column(
    #     bikereg_results_path=DATA_PATH + '/in/bikereg.csv',
    #     total_racers=180
    # )

    pipelines.add_new_racers_to_existing_csv(
        with_bib_nums_path=DATA_PATH + '/out/bikereg-deduped-with-bib-numbers.csv',
        racers_to_add_path=DATA_PATH + '/out/bikereg-deduped.csv',
        output_filepath=DATA_PATH + '/out/bikereg-deduped-with-bib-numbers-all-reg.csv'
    )

    # momma.validate_categories(
    #     bikereg_path=DATA_PATH + '/out/bikereg-deduped.csv'
    # )

    # pipelines.dedup_bikreg_category_merch_column(
    #     bikereg_results_path=DATA_PATH + '/in/bikereg-with-walk-up.csv',
    #     total_racers=137
    # )

    # pipelines.join_bikereg_csvs(
    #     pre_reg_bib_nums_path=DATA_PATH + '/out/bikereg-deduped-with-bib-numbers.csv',
    #     walk_up_path=DATA_PATH + '/out/bikereg-deduped.csv'
    # )

    # pipelines.join_webscorer_and_bikereg(
    #     webscorer_path=DATA_PATH + '/in/test/webscorer.csv',
    #     bikereg_path=DATA_PATH + '/out/bikereg-deduped-with-bib-numbers-all-reg.csv',
    #     staggered_time_marker_bibs=momma.MARKER_BIBS,
    #     strict_matching=False
    # )
    #
    # momma.time_transform(
    #     results_path=DATA_PATH + '/out/bikereg-deduped-with-bib-numbers-all-reg-with-times.csv',
    #     output_filename=DATA_PATH + '/out/final-results.csv'
    # )

    main()
