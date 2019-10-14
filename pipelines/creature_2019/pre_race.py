from pipelines import pipelines

DATA_PATH = '../../data/creature-2019-test'
BIKEREG_PATH = DATA_PATH + '/in/bikereg.csv'
TOTAl_RACERS = 33

pipelines.dedup_bikreg_category_merch_column(BIKEREG_PATH, TOTAl_RACERS)
pipelines.assign_bib_numbers(pipelines.no_merch_path(BIKEREG_PATH))
