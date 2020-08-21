def _format_num_lists(base_list, num_lists):
    """
    This function assumes that the numbers may not within the provided bases and may have leading zeros

    An example is [9000]. The value "9000" is greater than any of the given bases [24, 60] for 24 hour time
    """

    max_len = 0
    nums = []

    for a_num in num_lists:
        # remove negative sign
        is_negative = False
        x = 0

        for value in a_num:
            if value != 0: # ignore leading zeros
                if value < 0:
                    a_num = a_num[:x:-1] + [-a_num[x]]
                    is_negative = True
                else:
                    a_num = a_num[::-1]
                break
            x = x + 1

        # format numbers
        x = 0
        length = len(a_num)

        for value, base in zip(a_num, base_list):
            if value >= base:
                a_num[x] = value % base
                x = x + 1

                if x < length:
                    a_num[x] = a_num[x] + value // base
                else:
                    a_num.append(value // base)
                    length = length + 1
            else:
                x = x + 1

        # format negative numbers
        if is_negative:
            nums.append([-value for value in a_num])
        else:
            nums.append(a_num)

        # find length of the longest number
        if length > max_len:
            max_len = length

    # add trailing zeros so that all numbers are equal length
    return [a_num + (max_len - len(a_num)) * [0] if len(a_num) < max_len else a_num for a_num in nums]


def _format_num_lists_already_formatted(num_lists):
    """
    This function assumes that the numbers are already within the given bases and do not have leading zeros, or "already formated"

    An example is [1, 20]. All the values, "1" and "20", are less than the given bases [24, 60] for 24 hour time

    Replace any use of _format_num_lists() with this function if you know that you're only going to be dealing with already formatted numbers
    """

    max_len = 0
    nums = []

    for a_num in num_lists:
        # format negative numbers
        if a_num[0] < 0:
            a_num = [-value for value in reversed(a_num)]
            a_num[-1] = -a_num[-1]
            nums.append(a_num)
        else:
            nums.append(a_num[::-1])

        # find length of longest num
        length = len(a_num)

        if length > max_len:
            max_len = length

    # add trailing zeros so that all numbers are equal length
    return [a_num + (max_len - len(a_num)) * [0] if len(a_num) < max_len else a_num for a_num in nums]


def add(handle_most_sig_fig, base_list, num_lists):
    """
    Result: num_list_1 + num_list_2 + num_list_3 + ... + num_list_n
    This function returns a list representation of the number
    Ex: [2, 4] or [-2, 4] for negative answers

    num_lists is a list of the numbers to be added
    The numbers themselves are lists of values

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    The base list is aligned with the given numbers by the least significant digit
    It must be greater than or equal to the length of the two number lists

    Since the most significant digit can be outside the scope of the base list,
    handle_most_sig_fig is a boolean for whether or not the function should do any arithmetic on it
    Set it to true to treat it as if its base is the same as the most significant base in the base list
    Setting it to false will just leave the value appened to the front of the result
    """

    base_list = base_list[::-1]

    return _clean_up_bases(handle_most_sig_fig, base_list, [sum(x) for x in zip(*_format_num_lists(base_list, num_lists))])


def subtract(handle_most_sig_fig, base_list, num_lists):
    """
    Result: num_list_1 - num_list_2 - num_list_3 - ... - num_list_n
    This function returns a list representation of the number
    Ex: [2, 4] or [-2, 4] for negative answers

    num_lists is a list of the numbers to be subtracted
    The numbers themselves are lists of values

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    The base list is aligned with the given numbers by the least significant digit
    It must be greater than or equal to the length of the two number lists

    Since the most significant digit can be outside the scope of the base list,
    handle_most_sig_fig is a boolean for whether or not the function should do any arithmetic on it
    Set it to true to treat it as if its base is the same as the most significant base in the base list
    Setting it to false will just leave the value appened to the front of the result
    """

    base_list = base_list[::-1]

    return _clean_up_bases(handle_most_sig_fig, base_list, [x[0] - sum(x[1:]) for x in zip(*_format_num_lists(base_list, num_lists))])


def _clean_up_bases(handle_most_sig_fig, base_list, value_list):
    """
    This "cleans up" the result of the addition or subtraction to give the right answer to the operation

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function may or may not try to correct the carry or the -1 in the example depending on the boolean handle_most_sig_fig

    The list of bases must be greater than or equal to the length of the list of values
    """

    # check if it's a negative number and format it
    is_negative = False
    x = -1
    length = len(value_list)

    while x >= -length:
        val = value_list[x]
        if val != 0:
            if val < 0:
                is_negative = True
                value_list = [-value for value in value_list]
            break
        x = x - 1

    # compute the carries to get the correct result
    x = 0

    for value, base in zip(value_list, base_list):
        if value >= base or value < 0:
            value_list[x] = value % base
            x = x + 1

            if x < length:
                value_list[x] = value_list[x] + value // base # floor division
            else:
                value_list.append(value // base)
                length = length + 1
        else:
            x = x + 1

    # removing leading zeros
    x = -1

    while x >= -length:
        if value_list[x] != 0:
            if x != -1:
                value_list = value_list[:x + 1]
            break
        x = x - 1
    else:
        value_list = [0]

    # This section of code tries to correct the carry by using the most significant base
    if handle_most_sig_fig and length + x >= len(base_list):
        base = base_list[-1]
        value = value_list[-1]

        while value >= base:
            value_list[-1] = value % base
            value = value // base
            value_list.append(value)

    # add the negative sign
    if is_negative:
        value_list[-1] = -value_list[-1]

    value_list.reverse()

    return value_list


if __name__ == "__main__":
    '''
    Here is an example of how to use add() and subtract()

    Since I don't care if there is a carry or not, I set handle_most_sig_fig to False

    The list of bases is [24, 60] for 24 hour time

    The numbers, or time in this case, that I want to add together is 1:20 + 2 hours and 41 minutes
    and the numbers I want to subtract is 4:01 - 2 hours and 41 minutes
    '''

    print(add(False, [24, 60], [[1, 20], [2, 41]]))
    print(subtract(False, [24, 60], [[4, 1], [2, 41]]))
