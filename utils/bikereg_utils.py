CATEGORY_ENTERED = 'Category Entered'
CAT_AND_MERCH = 'Category Entered / Merchandise Ordered'
GENDER = 'Gender'
DISCIPLINES = {
    'xc': 'XC',
    'xcm': 'XCM',
    'enduro': 'ED'
}


def get_category_gender(row):
    cat = row[CATEGORY_ENTERED]
    cat_gender = None
    if 'Women' in cat:
        cat_gender = 'Women'
    elif 'Men' in cat:
        cat_gender = 'Men'
    else:
        gender = row[GENDER]
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


def get_race_class(row, categories):
    cat = row[CATEGORY_ENTERED]
    clazz = None
    for category in categories:
        if clazz is not None:
            break
        if f"{category} " in cat:
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
