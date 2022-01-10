def remove_zeroes (date_string):

    if date_string[0] == '0' and date_string[3] == '0':
        date_string = date_string[1:3] + date_string[4:]

    elif date_string[0] == '0':
        date_string = date_string[1:]

    elif date_string[0] != '0' and date_string[3] == '0':
        date_string = date_string[0:3] + date_string[4:]

    return date_string

