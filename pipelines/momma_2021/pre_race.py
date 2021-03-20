from pipelines import pipelines

# FIXME: this is a test directory
DATA_PATH = '../../data/momma-2019'
BIKEREG_PATH = DATA_PATH + '/in/bikereg.csv'
TOTAl_RACERS = 58
NUMBER_SEQUENCE_START = 501
NUMBER_SEQUENCE_END = 700


# stuff to run always here such as class/def
def main():
    pass


if __name__ == "__main__":
    # TODO: probably don't need this and can just use 'All entries for a person on a single row' in BikeReg
    # stuff only to run when not called via 'import' here
    # pipelines.dedup_bikreg_category_merch_column(
    #     bikereg_results_path=BIKEREG_PATH,
    #     total_racers=TOTAl_RACERS
    # )
    pipelines.assign_bib_numbers(
        bikereg_path=pipelines.in_dir(BIKEREG_PATH) + '.csv',
        sequence_start=NUMBER_SEQUENCE_START
    )
    main()
