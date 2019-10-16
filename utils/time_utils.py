def add_hours_digit(df):
    """
     Convert times to HH:MM:SS.S format with 0
    :param dataframe: dataframe to operate on
    :param rowname: name of the row with times
    :return the new dataframe
    """
    for index, row in df.iterrows():
        time = str(row['Time'])
        times = time.split(':')
        if len(times) == 2:
            df.loc[index, 'Time'] = '0:' + time

    return df


def row_time_to_secs(row):
    hrs, mins, secs = str(row['Time']).split(':')

    hrs_secs = int(hrs) * 60 * 60
    mins_secs = int(mins) * 60

    return float(hrs_secs + mins_secs + float(secs))
