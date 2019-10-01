CATEGORY_ENTERED = 'Category Entered'
CAT_AND_MERCH = 'Category Entered / Merchandise Ordered'

def get_category_gender(row):
    cat = row[CATEGORY_ENTERED]
    cat_gender = None
    if cat.conttains('Women'):
        cat_gender = 'Women'
    elif cat.contains('Men'):
        cat_gender = 'Men'
    try:
        assert not cat_gender is None
    except AssertionError as ass_err:
        ass_err.args += (
            'No gender can be extracted from Category: ',
            cat
        )
        raise

def get_cat(row):
    cat = row[CATEGORY_ENTERED]