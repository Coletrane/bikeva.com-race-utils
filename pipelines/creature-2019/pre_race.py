from pipelines import pipelines

BIKEREG_PATH = '../../data/creature-2019-test/bikereg-no-bibs.csv'
TOTAl_RACERS = 32

pipelines.dedup_bikreg_category_merch_column(BIKEREG_PATH, TOTAl_RACERS)

