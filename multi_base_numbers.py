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
        length = len(a_num) - 1

        a_num = a_num[::-1]

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

                if x < length:
                    a_num[x + 1] += carry
                else:
                    a_num += [carry]
                    length += 1

        nums.append(a_num)
        length += 1

        if length > max_len:
            max_len = length

    # add leading zeros so that all numbers are equal length
    return [a_num + [0 for _ in range(max_len - len(a_num))] for a_num in nums]


def add(clean_up_most_sig_fig, base_list, *num_lists):
    """
    num_list_1 + num_list_2

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    It must be greater than or equal to the length of the two number lists
    """

    base_list = base_list[::-1]

    return _clean_up_bases(clean_up_most_sig_fig, base_list, [sum(x) for x in zip(*_format_num_lists(base_list, num_lists))])


def subtract(clean_up_most_sig_fig, base_list, *num_lists):
    """
    num_list_1 - num_list_2

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    It must be greater than or equal to the length of the two number lists
    """

    base_list = base_list[::-1]

    return _clean_up_bases(clean_up_most_sig_fig, base_list, [x[0] - sum(x[1:]) for x in zip(*_format_num_lists(base_list, num_lists))])


def _clean_up_bases(clean_up_most_sig_fig, base_list, value_list):
    """
    This "cleans up" the result of the addition or subtraction to give the right answer to the operation

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function may or may not try to correct the carry or the -1 in the example depending on clean_up_most_sig_fig

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

    length = len(value_list) - 1

    for x, (value, base) in enumerate(zip(value_list, base_list)):
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
            value_list = value_list[x:]
            break
    else:
        value_list = [0]

    # This section of code tries to correct the carry by extending the list of bases using the most significant base
    if clean_up_most_sig_fig and length + 1 > len(base_list):
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
    # here is an example
    print(add(False, [24, 60], [1, 20], [2, 41]))
