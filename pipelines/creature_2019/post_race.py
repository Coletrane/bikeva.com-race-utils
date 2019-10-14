# Run this file AFTER entering walk up registration into BikeReg and re-exporting it

from pipelines.creature_2019 import pre_race
from pipelines import pipelines

BIB_NUMBERS_PATH = pipelines.bib_numbers_path(pre_race.BIKEREG_PATH),

pipelines.join_bikereg_csvs(
    pipelines.bib_numbers_path(pre_race.BIKEREG_PATH),
    pre_race.DATA_PATH + '/in/bikereg-with-walk-up.csv'
)
pipelines.join_webscorer_and_bikereg(
    pre_race.DATA_PATH + '/in/webscorer.txt',
    pipelines.bikereg_join_path(BIB_NUMBERS_PATH)
)