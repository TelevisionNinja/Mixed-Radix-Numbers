def _pad_left(a_list, length):
    """
    pad zeros to the left of a list
    """

    return [0 for _ in range(length - len(a_list))] + a_list


def _remove_leading_element(a_list):
    for x, value in enumerate(a_list):
        if value != 0:
            return a_list[x:]

    return [0]


def _compare_nums(num_lists):
    """
    compares two numbers that are represented as lists

    both lists must be the same length

    1 : list 1 is greater
    0 : both are equal
    -1 : list 2 is greater
    """

    for l in zip(*num_lists):
        val_1 = l[0]
        val_2 = sum(l[1:])

        if val_2 > val_1:
            return -1
        if val_1 > val_2:
            return 1

    return 0


def _format_list(num_lists):
    nums = []
    max_len = 0

    for l in num_lists:
        l = _format_num(l)
        nums.append(l)
        length = len(l)
        if length > max_len:
            max_len = length

    for x, l in enumerate(nums):
        nums[x] = _pad_left(l, max_len)

    return nums


def _format_num(a_list):
    # remove leading zeros
    if a_list[0] == 0:
        a_list = _remove_leading_element(a_list)

    # check if the number is negative
    if a_list[0] < 0:
        # make the whole list negative
        return [-x if x > 0 else x for x in a_list]

    return a_list


def add(base_list, *num_lists):
    """
    num_list_1 + num_list_2

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    It must be greater than or equal to the length of the two number lists
    """

    return clean_up_bases(base_list, [sum(x) for x in zip(*_format_list(num_lists))])


def subtract(base_list, *num_lists):
    """
    num_list_1 - num_list_2

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    It must be greater than or equal to the length of the two number lists
    """

    # format numbers
    nums = _format_list(num_lists)

    # compare the 1st number against the rest
    comparison = _compare_nums(nums)

    values = []

    if comparison == 1:
        values = [l[0] - sum(l[1:]) for l in zip(*nums)]
    elif comparison == -1:
        values = [sum(l[1:]) - l[0] for l in zip(*nums)]
    else:
        return [0]

    result = clean_up_bases(base_list, values)

    if comparison == -1:
        result[0] *= -1

    return result


def clean_up_bases(base_list, a_list):
    """
    This "cleans up" the result of the addition or subtraction to give the right answer to the operation

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function tries to correct the carry by extending the list of bases using the most significant base
    
    The list of bases must be greater than or equal to the length of the list of values

    The list of values must not have leading zeros
    """

    a_list = clean_up_bases_ignore_most_significant_digit(base_list, a_list)

    if len(a_list) > len(base_list):
        base = base_list[0]
        value = a_list[0]

        while abs(value) >= base:
            carry = value // base

            if value < 0:
                value *= -1
                carry = -(value // base)

            a_list.insert(0, carry)
            a_list[1] = value % base

            value = carry

    return a_list


def clean_up_bases_ignore_most_significant_digit(base_list, a_list):
    """
    This "cleans up" the result of the addition or subtraction to give the right answer to the operation

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function will not try to correct the carry or the -1 in the example

    The list of bases must be greater than or equal to the length of the list of values

    The list of values must not have leading zeros
    """

    # check if it's a negative number and correctly format it
    negative_flag = True

    for x in a_list:
        if x > 0:
            negative_flag = False
            break
    else:
        a_list = [-x for x in a_list]

    a_list.reverse()
    base_list.reverse()

    length = len(a_list) - 1

    for x, (value, base) in enumerate(zip(a_list, base_list)):
        if value >= base or value < 0:
            carry = value // base # floor division is necessary

            if -value >= base:
                value *= -1
                carry = -(value // base)

            a_list[x] = value % base

            if x < length:
                a_list[x + 1] += carry
            else:
                a_list += [carry]
                length += 1

    a_list.reverse()
    base_list.reverse()

    # removing leading zeros
    if a_list[0] == 0:
        a_list = _remove_leading_element(a_list)

    if negative_flag:
        a_list[0] *= -1

    return a_list


if __name__ == "__main__":
    # here is an example
    print(add([24, 60], [1, 20], [2, 41]))
