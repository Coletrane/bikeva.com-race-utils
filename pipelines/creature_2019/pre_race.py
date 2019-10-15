from pipelines import pipelines

DATA_PATH = '../../data/creature-2019-test'
BIKEREG_PATH = DATA_PATH + '/in/bikereg.csv'
TOTAl_RACERS = 31
NUMBER_SEQUENCE_START = 500
NUMBER_SEQUENCE_END = 700


# stuff to run always here such as class/def
def main():
    pass


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    pipelines.dedup_bikreg_category_merch_column(
        bikereg_results_path=BIKEREG_PATH,
        total_racers=TOTAl_RACERS
    )
    pipelines.assign_bib_numbers(
        bikereg_path=pipelines.out_dir(BIKEREG_PATH) + '.csv',
        sequence_start=NUMBER_SEQUENCE_START
    )
    main()
