# Run this file AFTER entering walk up registration into BikeReg and re-exporting it

from pipelines import pipelines
from utils import race_utils_common as race_utils
from utils import momma_utils as momma

# TODO: this is a test directory
DATA_PATH = '../../data/momma-2021-test'
BIKEREG_PATH = DATA_PATH + '/in/bikereg.csv'


# stuff to run always here such as class/def
def main():
    pass


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here

    # pipelines.dedup_bikreg_category_merch_column(
    #     bikereg_results_path=DATA_PATH + '/in/bikereg.csv',
    #     total_racers=52
    # )

    # pipelines.dedup_bikreg_category_merch_column(
    #     bikereg_results_path=DATA_PATH + '/in/bikereg-with-walk-up.csv',
    #     total_racers=80
    # )

    # pipelines.join_bikereg_csvs(
    #     pre_reg_bib_nums_path=DATA_PATH + '/out/bikereg-deduped.csv',
    #     walk_up_path=DATA_PATH + '/out/bikereg-with-walk-up-deduped.csv'
    # )

    pipelines.join_webscorer_and_bikereg(
        webscorer_path=DATA_PATH + '/in/webscorer.csv',
        bikereg_path=DATA_PATH + '/out/bikereg-deduped-all-reg.csv',
        staggered_time_marker_bibs=[race_utils.XC_START_MARKER_BIB_NUMBER]
    )

    # momma.time_transform(
    #     results_path=DATA_PATH + '/out/bikereg-deduped-all-reg-with-times.csv'
    # )

    main()
