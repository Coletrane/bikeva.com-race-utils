# Run this file AFTER entering walk up registration into BikeReg and re-exporting it

from pipelines import pipelines
from pipelines.creature_2019 import pre_race
from utils import creature_utils as creature

BIKEREG_WITH_WALKUP_PATH = pre_race.DATA_PATH + '/in/bikereg-with-walk-up.csv'
TOTAL_RACERS_WITH_WALKUP = 33

BIB_NUMBERS_PATH = pipelines.bib_numbers_path(pre_race.BIKEREG_PATH)
BIKEREG_JOIN_PATH = pipelines.bikereg_join_path(BIB_NUMBERS_PATH)
WEBSCORER_BIKEREG_JOIN_PATH = pipelines.webscorer_bikereg_join_path(BIKEREG_JOIN_PATH)


# stuff to run always here such as class/def
def main():
    pass


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    pipelines.dedup_bikreg_category_merch_column(
        bikereg_results_path=BIKEREG_WITH_WALKUP_PATH,
        total_racers=TOTAL_RACERS_WITH_WALKUP
    )
    pipelines.join_bikereg_csvs(
        pre_reg_bib_nums_path=BIB_NUMBERS_PATH,
        walk_up_path=pipelines.out_dir(BIKEREG_WITH_WALKUP_PATH) + '.csv'
    )
    pipelines.join_webscorer_and_bikereg(
        webscorer_path=pre_race.DATA_PATH + '/in/webscorer.txt',
        bikereg_path=BIKEREG_JOIN_PATH,
        staggered_time_marker_bibs=[creature.XC_START_MARKER_BIB_NUMBER]
    )
    creature.time_transform(
        results_path=WEBSCORER_BIKEREG_JOIN_PATH
    )
    main()
