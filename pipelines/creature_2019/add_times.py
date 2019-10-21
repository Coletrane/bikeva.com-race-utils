from pipelines import pipelines
from pipelines.creature_2019 import post_race
from pipelines.creature_2019 import pre_race
from utils import creature_utils as creature


def main():
    pass


if __name__ == "__main__":
    pipelines.join_webscorer_and_bikereg(
        webscorer_path=pre_race.DATA_PATH + '/in/webscorer.txt',
        bikereg_path=post_race.BIKEREG_JOIN_PATH,
        staggered_time_marker_bibs=[creature.XC_START_MARKER_BIB_NUMBER]
    )
    creature.time_transform(
        results_path=post_race.WEBSCORER_BIKEREG_JOIN_PATH
    )
    main()
