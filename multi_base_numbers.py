def _pad_left(num, length):
    """
    pad zeros to the left of a list
    """

    return [0 for _ in range(length - len(num))] + num


def _format_num_lists(base_list, num_lists):
    nums = []
    max_len = 0

    for a_num in num_lists:
        # ignore leading zeros and format negative numbers
        for x in a_num:
            if x != 0:
                if x < 0:
                    a_num = [-x if x > 0 else x for x in a_num]
                break

        # clean up numbers
        a_num = clean_up_num_ignore_most_significant_digit(base_list, a_num)

        nums.append(a_num)
        length = len(a_num)

        if length > max_len:
            max_len = length

    return [_pad_left(a_num, max_len) for a_num in nums]


def add(base_list, *num_lists):
    """
    num_list_1 + num_list_2

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    It must be greater than or equal to the length of the two number lists
    """

    return _clean_up_bases(base_list, [sum(x) for x in zip(*_format_num_lists(base_list, num_lists))])


def subtract(base_list, *num_lists):
    """
    num_list_1 - num_list_2

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    It must be greater than or equal to the length of the two number lists
    """

    return _clean_up_bases(base_list, [x[0] - sum(x[1:]) for x in zip(*_format_num_lists(base_list, num_lists))])


def _clean_up_bases(base_list, value_list):
    """
    This "cleans up" the result of the addition or subtraction to give the right answer to the operation

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function tries to correct the carry by extending the list of bases using the most significant base
    
    The list of bases must be greater than or equal to the length of the list of values

    The list of values must not have leading zeros
    """

    value_list = _clean_up_bases_ignore_most_significant_digit(base_list, value_list)

    if len(value_list) > len(base_list):
        base = base_list[0]
        value = value_list[0]

        while abs(value) >= base:
            carry = value // base

            if value < 0:
                value *= -1
                carry = -(value // base)

            value_list.insert(0, carry)
            value_list[1] = value % base

            value = carry

    return value_list


def _clean_up_bases_ignore_most_significant_digit(base_list, value_list):
    """
    This "cleans up" the result of the addition or subtraction to give the right answer to the operation

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function will not try to correct the carry or the -1 in the example

    The list of bases must be greater than or equal to the length of the list of values

    The list of values must not have leading zeros
    """

    # check if it's a negative number and format it
    negative_flag = False

    for x in value_list:
        if x != 0:
            if x < 0:
                negative_flag = True
                value_list = [-x for x in value_list]
            break

    length = len(value_list) - 1

    value_list.reverse()

    for x, (value, base) in enumerate(zip(value_list, reversed(base_list))):
        if value >= base or value < 0:
            carry = value // base  # floor division
            value_list[x] = value % base

            if x < length:
                value_list[x + 1] += carry
            else:
                value_list += [carry]
                length += 1

    value_list.reverse()

    # removing leading zeros
    for x, value in enumerate(value_list):
        if value != 0:
            if negative_flag:
                value_list[x] *= -1
            return value_list[x:]

    return [0]


def clean_up_num(base_list, num):
    """
    This "cleans up" the given multi-base number

    This may or may not return leading zeros

    Negative numbers are represented as a list of negative values

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function tries to correct the carry by extending the list of bases using the most significant base
    
    The list of bases must be greater than or equal to the length of the number
    """

    num = clean_up_num_ignore_most_significant_digit(base_list, num)

    if len(num) > len(num):
        base = base_list[0]
        value = num[0]

        while abs(value) >= base:
            carry = value // base

            if value < 0:
                value *= -1
                carry = -(value // base)

            num.insert(0, carry)
            num[1] = value % base

            value = carry

    return num


def clean_up_num_ignore_most_significant_digit(base_list, num):
    """
    This "cleans up" the given multi-base number

    This may or may not return leading zeros

    Negative numbers are represented as a list of negative values

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function will not try to correct the carry or the -1 in the example

    The list of bases must be greater than or equal to the length of the number
    """

    length = len(num) - 1

    num.reverse()

    for x, (value, base) in enumerate(zip(num, reversed(base_list))):
        if abs(value) >= base:
            is_negative = False
            if value < 0:
                value *= -1
                is_negative = True

            carry = value // base
            num[x] = value % base

            if is_negative:
                num[x] *= -1
                carry *= -1

            if x < length:
                num[x + 1] += carry
            else:
                num += [carry]
                length += 1

    num.reverse()

    return num


if __name__ == "__main__":
    # here is an example
    print(add([24, 60], [1, 20], [2, 41]))
