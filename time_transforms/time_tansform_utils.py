def add_hours_digit(dataframe, rowname):
    """
     Convert times to HH:MM:SS.S format with 0
    :param dataframe: dataframe to operate on
    :param rowname: name of the row with times
    :return the new dataframe
    """
    for row in dataframe[rowname].itterows():
        times = row.split(':')
        if len(times) == 2:
            row = f'0:{row}'

    return dataframe

def hrs_and_mins_to_secs(hrs, mins):
    """
    Convert hours and minutes to a combined seconds value
    :param hrs: int
    :param mins: int
    :return: imt hours + minutes in seconds
    """
    hrs_secs = hrs * 60 * 60
    mins_secs = mins * 60
    return hrs_secs + mins_secs