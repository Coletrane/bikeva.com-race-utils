from pipelines import pipelines

DATA_PATH = '../../data/creature-2019-test'
BIKEREG_PATH = DATA_PATH + '/in/bikereg.csv'
TOTAl_RACERS = 33
NUMBER_SEQUENCE_START = 500
NUMBER_SEQUENCE_END = 700

pipelines.dedup_bikreg_category_merch_column(
    bikereg_results_path=BIKEREG_PATH,
    total_racers=TOTAl_RACERS
)
pipelines.assign_bib_numbers(
    bikereg_path=pipelines.no_merch_path(BIKEREG_PATH),
    sequence_start=NUMBER_SEQUENCE_START
)
