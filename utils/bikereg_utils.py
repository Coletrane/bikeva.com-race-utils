import pandas as pd

CATEGORY_ENTERED = 'Category Entered'
CAT_AND_MERCH = 'Category Entered / Merchandise Ordered'

DISCIPLINES = {
    'xc': 'XC',
    'xcm': 'XCM',
    'enduro': 'ED'
}


def get_dtypes(with_merch=False):
    dtypes = {
        'Bib': pd.Int64Dtype(),
        'City': str,
        'First Name': str,
        'USAC License Status': str,
        'Last Name': str,
        'State': str,
        'Team': str,
        'USAC License': str,
        'Age on Event Day': str,
        'Email': str,
        'Phone': str,
        'USAC Category XC': str,
        'USAC Category DH': str,
        'Category Date': str,
        'Gender': str,
        'Quantity': pd.Int64Dtype()
    }
    if with_merch:
        dtypes[CAT_AND_MERCH]: str
    else:
        dtypes[CATEGORY_ENTERED]: str

    return dtypes


def read_csv_with_dtypes(filepath, dtypes=None):
    if dtypes is None:
        dtypes = get_dtypes()
    return pd.read_csv(
        filepath,
        header=0,
        dtype=dtypes
    )


def get_category_gender(row):
    cat = row[CATEGORY_ENTERED]
    cat_gender = None
    if 'Women' in cat:
        cat_gender = 'Women'
    elif 'Men' in cat:
        cat_gender = 'Men'
    else:
        gender = row['Gender']
        if gender == 'X':
            gender = 'Both'
        cat_gender = gender
    try:
        assert not cat_gender is None
    except AssertionError as ass_err:
        ass_err.args += (
            'No gender can be extracted from Category: ',
            cat
        )
        raise

    return cat_gender


def get_race_cat(row):
    cat = row[CATEGORY_ENTERED] \
        .split('Cat')[1] \
        .split(' ')[1]
    try:
        assert not cat is None
        return cat
    except AssertionError as ass_err:
        ass_err.args += (
            'No cat numbers can be extracted from Category: ',
            row[CATEGORY_ENTERED]
        )
        raise


def get_race_class(row, disciplines):
    cat = row[CATEGORY_ENTERED]
    clazz = None
    for category in disciplines:
        if clazz is not None:
            break
        if get_race_discipline(row, disciplines) is not None:
            clazz = cat \
                .replace(category, '') \
                .replace(f"Cat {get_race_cat(row)}", '')

    try:
        assert clazz is not None
        return clazz
    except AssertionError as ass_err:
        ass_err.args += (
            'No class can be extracted from Category: ',
            cat
        )
        raise


def get_race_discipline(row, disciplines):
    cat = row[CATEGORY_ENTERED]
    for discipline in disciplines:
        if f"{discipline} " in cat:
            return discipline


def get_race_age_group(row, discipline_age_groups):
    cat = row[CATEGORY_ENTERED]
    discipline = get_race_discipline(row, list(discipline_age_groups.keys()))
    age_groups = discipline_age_groups[discipline]
    found_age_group = None
    for age_group in age_groups:
        if found_age_group is not None:
            break
        if age_group in cat:
            found_age_group = age_group

    # may need to use row[AGE_ON_EVENT_DAY] here to discern age group?
    if found_age_group is None:
        found_age_group = 'Open'

    return found_age_group
