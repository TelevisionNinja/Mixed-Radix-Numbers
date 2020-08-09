def _format_num_lists(base_list, num_lists):
    """
    This function assumes that the numbers may not within the provided bases and may have leading zeros

    An example is [9000]. The value is greater the given bases [24, 60]
    """

    max_len = 0
    nums = []

    for a_num in num_lists:
        # ignore leading zeros and format negative numbers
        for x in a_num:
            if x != 0:
                if x < 0:
                    a_num = [-x if x > 0 else x for x in reversed(a_num)]
                else:
                    a_num = a_num[::-1]
                break

        # format numbers
        length = len(a_num)

        for x, (value, base) in enumerate(zip(a_num, base_list)):
            if abs(value) >= base:
                is_negative = False

                if value < 0:
                    value *= -1
                    is_negative = True

                carry = value // base
                a_num[x] = value % base

                if is_negative:
                    a_num[x] *= -1
                    carry *= -1

                x += 1

                if x < length:
                    a_num[x] += carry
                else:
                    a_num += [carry]
                    length += 1

        nums.append(a_num)

        # find length of longest num
        if length > max_len:
            max_len = length

    # add trailing zeros so that all numbers are equal length
    return [a_num + [0 for _ in range(max_len - len(a_num))] if len(a_num) < max_len else a_num for a_num in nums]


def _format_num_lists_already_formatted(num_lists):
    """
    This function assumes that the numbers are already within the given bases and do not have leading zeros, or "already formated"

    An example is [1, 20]. All the values are less than the given bases [24, 60]

    Replace any use of _format_num_lists() with this function if you know that you're only going to be dealing with already formatted numbers
    """

    max_len = 0

    for y, a_num in enumerate(num_lists):
        # format negative numbers
        if a_num[0] < 0:
            num_lists[y] = [-x if x > 0 else x for x in reversed(a_num)]
        else:
            num_lists[y] = a_num[::-1]

        length = len(a_num)

        # find length of longest num
        if length > max_len:
            max_len = length

    # add trailing zeros so that all numbers are equal length
    return [a_num + [0 for _ in range(max_len - len(a_num))] if len(a_num) < max_len else a_num for a_num in num_lists]


def add(handle_most_sig_fig, base_list, num_lists):
    """
    Result: num_list_1 + num_list_2 + num_list_3 + ... + num_list_n

    num_lists is a list of the numbers to be added
    The numbers themselve are lists of values

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

    num_lists is a list of the numbers to be subtracted
    The numbers themselve are lists of values

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

    The list of values must not have leading zeros
    """

    # check if it's a negative number and format it
    negative_flag = False

    for x in reversed(value_list):
        if x != 0:
            if x < 0:
                negative_flag = True
                value_list = [-x for x in value_list]
            break

    # compute correct result
    for x, (value, base) in enumerate(zip(value_list, base_list)):
        if value >= base or value < 0:
            value_list[x] = value % base

            x += 1

            if x < len(value_list):
                value_list[x] += value // base # floor division
            else:
                value_list += [value // base]

    value_list.reverse()

    # removing leading zeros
    for x, value in enumerate(value_list):
        if value != 0:
            if negative_flag:
                value_list[x] *= -1
            value_list = value_list[x:]
            break
    else:
        value_list = [0]

    # This section of code tries to correct the carry by using the most significant base
    if handle_most_sig_fig and len(value_list) > len(base_list):
        base = base_list[-1]
        value = value_list[0]

        while abs(value) >= base:
            carry = value // base

            if value < 0:
                value *= -1
                carry = -(value // base)

            value_list[0] = value % base
            value_list.insert(0, carry)
            value = carry

    return value_list


if __name__ == "__main__":
    '''
    Here is an example of how to use add()

    Since I don't care if there is a carry or not, I set handle_most_sig_fig to False

    The list of bases is [24, 60] for 24 hour time

    The numbers, or time in this case, that I want to add together is 1:20 + 2 hours and 41 minutes
    '''

    print(add(False, [24, 60], [[1, 20], [2, 41]]))
