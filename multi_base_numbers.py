def _pad_left(num, length):
    """
    pad zeros to the left of a list
    """

    return [0 for _ in range(length - len(num))] + num


def _remove_leading_zeros(num):
    for x, value in enumerate(num):
        if value != 0:
            return num[x:]

    return [0]


def _compare_nums(num_lists):
    """
    compares numbers that are represented as lists

    both lists must be the same length

    1 : list 1 is greater
    0 : both are equal
    -1 : list 2-n is greater
    """

    for values in zip(*num_lists):
        val_1 = values[0]
        val_2 = sum(values[1:])

        if val_2 > val_1:
            return -1
        if val_1 > val_2:
            return 1

    return 0


def _format_list(num_lists):
    nums = []
    max_len = 0

    for a_num in num_lists:
        a_num = _format_num(a_num)
        nums.append(a_num)
        length = len(a_num)
        if length > max_len:
            max_len = length

    for x, a_num in enumerate(nums):
        nums[x] = _pad_left(a_num, max_len)

    return nums


def _format_num(num):
    # remove leading zeros
    if num[0] == 0:
        num = _remove_leading_zeros(num)

    # check if the number is negative
    if num[0] < 0:
        # make the whole list negative
        return [-x if x > 0 else x for x in num]

    return num


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

    result = []

    if comparison == 1:
        result = [values[0] - sum(values[1:]) for values in zip(*nums)]
    elif comparison == -1:
        result = [sum(values[1:]) - values[0] for values in zip(*nums)]
    else:
        return [0]

    result = clean_up_bases(base_list, result)

    if comparison == -1:
        result[0] *= -1

    return result


def clean_up_bases(base_list, value_list):
    """
    This "cleans up" the result of the addition or subtraction to give the right answer to the operation

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function tries to correct the carry by extending the list of bases using the most significant base
    
    The list of bases must be greater than or equal to the length of the list of values

    The list of values must not have leading zeros
    """

    value_list = clean_up_bases_ignore_most_significant_digit(base_list, value_list)

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


def clean_up_bases_ignore_most_significant_digit(base_list, value_list):
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

    for x in value_list:
        if x > 0:
            negative_flag = False
            break
    else:
        value_list = [-x for x in value_list]

    value_list.reverse()
    base_list.reverse()

    length = len(value_list) - 1

    for x, (value, base) in enumerate(zip(value_list, base_list)):
        if value >= base or value < 0:
            carry = value // base  # floor division is necessary

            if -value >= base:
                value *= -1
                carry = -(value // base)

            value_list[x] = value % base

            if x < length:
                value_list[x + 1] += carry
            else:
                value_list += [carry]
                length += 1

    value_list.reverse()
    base_list.reverse()

    # removing leading zeros
    if value_list[0] == 0:
        value_list = _remove_leading_zeros(value_list)

    if negative_flag:
        value_list[0] *= -1

    return value_list


if __name__ == "__main__":
    # here is an example
    print(add([24, 60], [1, 20], [2, 41]))
