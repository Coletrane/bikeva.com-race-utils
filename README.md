# BikeVA.com Race Utilities

### https://bikeva.com

## Webscorer Pipeline:

While Webscorer as an app provides extensive features, the user experience is confusing and dated.
Transferring start lists via iTunes rarely works, and uploading them to the Webscorer website is
less than streamlined. Additionally, Webscorer PRO is neither a cost I would like to incur, nor do I
feel the product commands the price.

~~Mark my words, Webscorer's iPad only timing (no chips/RFC features) is _highly disruptible_~~

Edit 4/10/21 Zone4.ca is that disruptor

I digress.

### Pre Raceday (`pre_race.py`):

1. **If you have sequential numbers:**

`assign_bib_numbers.py` Run before the race and is the __single source of truth__ for assigned bib
numbers. Use the assigned bib numbers when writing names on bibs and number plates. * __Input:__
BikeReg registration list `.csv` file. * __Output:__ registration list `.csv` file with bib numbers.

**If you do not have sequential numbers:**

Download the BikeReg registration file and manually match up names with numbers when preparing
pre-race pickup packets.

### Post Raceday (`post_race.py`):

0. `pipelines#dedup_bikereg_category_merch_column` _For some reason_, BikeReg thinks it's a great idea to
   combine the Category Entered and Merchandise Ordered columns into one. **Do not use the "All
   entries for a person on a single row" option when exporting from BikeReg.** We don't care about
   merchandise in this project, so run this before any script with raw input from BikeReg.
    * __Input:__ BikeReg registration list `.csv` file.
    * __Output:__ registration list `bikereg-deduped.csv` file with no duplicated rider names.
1. Add walk up registrations to BikeReg for reporting and export the full registration list `.csv`
   file.
2. Manually add walk up registration bib numbers.
    * __Thank you COVID for destroying walk up registration.__ There will likely be _some_ walk ups,
      since we don't want to turn anybody down, day of, but we're not advertising them as available.
3. `pipelines#join_bikereg_csvs` Run after the race to get walk up registrations in the registration list.
    * __Input:__
        * Output `.csv` from `assign_bib_numbers.py`.
        * BikeReg registration list `.csv` that includes walk up Registrations and manually entered
    * __Output:__ `.csv` joined on First Name, Last Name, and Category.
4. `pipelines#join_webscorer_and_bikereg`
    * __Input:__
        * Webscorer tab delimited text file with bib numbers and times
        * Output from `join_bikereg_csvs.py`
    * __Output:__ Full registration `.csv` with _raw_ times
5. `<race-name>_utils.py#time_transform`
    * __Input:__ Output from `webscorer_txt_join_bikereg_csv_on_bib_column.py`
    * __Output:__ `.csv` file with adjusted times