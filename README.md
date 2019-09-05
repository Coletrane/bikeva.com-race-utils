# Virginia Championship Commission Race Utilities
### https://bikeva.com

## Webscorer Pipeline:
While Webscorer as an app provides extensive features, the user experience is confusing and dated. Transferring start lists via iTunes rarely works, and uploading them to the Webscorer website is less than streamlined. Additionally, Webscorer PRO is neither a cost I would like to incur, nor do I feel the product commands the price. 

Mark my words, Webscorer's iPad only timing (no chips/RFC features) is _highly disputable_

I digress.

1. `assign_bib_numbers.py` Run before the race and is the __single source of truth__ for assigned bib numbers. Use the assigned bib numbers when writing names on bibs and number plates.
    * __Input:__ BikeReg registration list `.csv` file.
    * __Output:__ registration list `.csv` file with bib numbers.   
2. Add walk up registrations to BikeReg for reporting and export the full registration list `.csv` file.
3. Manually add walk up registration bib numbers.
4. `join_bikereg_csvs.py` Run after the race to get walk up registrations in the registration list.
    * __Input:__ 
        * Output `.csv` from `assign_bib_numbers.py`.
        * BikeReg registration list `.csv` that includes walk up Registrations and manually entered 
    * __Output:__ `.csv` joined on First Name, Last Name, and Category.
5.  `webscorer_txt_join_bikereg_csv_on_bib_column.py` 
    * __Input:__ 
        * Webscorer tab delimited text file with bib numbers and times
        * Output from `join_bikereg_csvs.py`
    * __Output:__ Full registration `.csv` with _raw_ times
6. `/time_Transforms` 
    * __Input:__ Output from `webscorer_txt_join_bikereg_csv_on_bib_column.py`
    * __Output:__ `.csv` file with adjusted times