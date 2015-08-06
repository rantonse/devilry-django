from django import template
import os.path
register = template.Library()

@register.filter("devilry_truncatefileextension")
def devilry_truncatefileextension(value, max_length):
    """
    max_length is the number of characters the truncated
    string consists of including the extension
    Example:  if max_length is 10, the string "Delivery.pdf" will be
               truncated to "Deli...pdf"
    Three letters from the filename will be showed either way.
    """
    if len(value) == 0:
        return 'NO_NAME'
    else:
        offset = 3              # show at least three letters from filename
        min_value_length = 8    # entire value name is same length or less than ex. Del.html

        if len(value) <= min_value_length:
            return value
        elif len(value) > max_length:
            splitted = os.path.splitext(value)
            value_extension = splitted[1].strip('.')   # get extension

            if (max_length - len(value_extension) - 3) < offset:
                # show at least three letters from valuename
                # to ensure no files are called "...<fileextension>"
                truncated_value = value[:offset] + '...' + value_extension
            else:
                truncated_value = value[:max_length - len(value_extension) - 3] + '...' + value_extension
            return truncated_value

    return value



@register.filter("devilry_verbosenumber")
def devilry_verbosenumber(value, number):
    """
    Numbers from 1 to 10 is given as verbose(first, second, third, ...)
    and all numbers above 10 has the number and the corresponding ending(11th, 23rd, 32nd, 41st, ...)
    """
    numbers = {
        1: 'FIRST', 2: 'SECOND', 3: 'THIRD', 4: 'FOURTH', 5: 'FIFTH',
        6: 'SIXTH', 7: 'SEVENTH', 8: 'EIGHTH', 9: 'NINTH', 10: 'TENTH'
    }

    def last_digit(num):
        # returns the last or two last numbers.
        n = str(num)
        if n[len(n)-2] is '1':
            # return the last two digits if number is
            # from 11 to 19 to get th-ending.
            return int(n[len(n)-1]+n[len(n)-2])
        return int(n[len(n)-1])

    if number <= 10:
        # use numbers dictionary
        # to get verbose result
        return numbers[number]
    elif number <= 19:
        # all numbers between 10 and 20 ends with th.
        return str(number)+'th'
    else:
        # handle numbers over 19
        n = last_digit(number)
        if n > 3 or n == 0:
            return str(number)+'th'
        return {
            1: str(number)+'st',
            2: str(number)+'nd',
            3: str(number)+'rd',
        }[n]