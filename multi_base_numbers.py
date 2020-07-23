def _pad_left(a_list, length):
    """
    pad zeros to the left of a list
    """

    new_list = [0 for _ in range(length - len(a_list))]
    new_list += a_list
    return new_list


def _remove_leading_element(a_list):
    for x, value in enumerate(a_list):
        if value != 0:
            return a_list[x:]

    return [0]


def _compare_numbers_represented_as_arrays(list_1, list_2):
    """
    compares two numbers that are represented as lists

    both lists must be the same length

    1 : list 1 is greater
    0 : both are equal
    -1 : list 2 is greater
    """

    for value_1, value_2 in zip(list_1, list_2):
        if value_2 > value_1:
            return -1
        if value_1 > value_2:
            return 1

    return 0


def _check_if_negative(a_list):
    if a_list[0] < 0:
        # make the whole list negative
        return [-x if x > 0 else x for x in a_list]
    return a_list


def add(num_list_1, num_list_2, base_list):
    """
    num_list_1 + num_list_2

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    It must be greater than or equal to the length of the two number lists
    """

    # format numbers
    num_list_1 = _check_if_negative(num_list_1)
    num_list_2 = _check_if_negative(num_list_2)

    length_1 = len(num_list_1)
    length_2 = len(num_list_2)

    if length_1 != length_2:
        max_len = max(length_1, length_2)

        num_list_1 = _pad_left(num_list_1, max_len)
        num_list_2 = _pad_left(num_list_2, max_len)

    return clean_up_bases([x + y for x, y in zip(num_list_1, num_list_2)], base_list)


def subtract(num_list_1, num_list_2, base_list):
    """
    num_list_1 - num_list_2

    base_list is a list of the bases of the 2 numbers this function is supposed to work with
    It must be greater than or equal to the length of the two number lists
    """

    # format numbers
    num_list_1 = _check_if_negative(num_list_1)
    num_list_2 = _check_if_negative(num_list_2)

    length_1 = len(num_list_1)
    length_2 = len(num_list_2)

    if length_1 != length_2:
        max_len = max(length_1, length_2)

        num_list_1 = _pad_left(num_list_1, max_len)
        num_list_2 = _pad_left(num_list_2, max_len)

    comparison = _compare_numbers_represented_as_arrays(num_list_1, num_list_2)

    if comparison == -1:
        num_list_1, num_list_2 = num_list_2, num_list_1

    result = clean_up_bases([x - y for x, y in zip(num_list_1, num_list_2)], base_list)

    if comparison == -1:
        result[0] *= -1

    return result


def clean_up_bases(a_list, base_list):
    """
    This "cleans up" the result of the addition or subtraction to give the right answer to the operation

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function tries to correct the carry by extending the list of bases using the most significant base
    
    The list of bases must be greater than or equal to the length of the list of values
    """

    a_list = clean_up_bases_ignore_most_significant_digit(a_list, base_list)

    if len(a_list) > len(base_list):
        while abs(a_list[0]) >= base_list[0]:
            carry = 0

            if a_list[0] < 0:
                a_list[0] *= -1
                carry = -(a_list[0] // base_list[0])
            else:
                carry = a_list[0] // base_list[0]

            a_list.insert(0, carry)
            a_list[1] = a_list[1] % base_list[0]

    return a_list


def clean_up_bases_ignore_most_significant_digit(a_list, base_list):
    """
    This "cleans up" the result of the addition or subtraction to give the right answer to the operation

    Since there is a chance the list of bases is not long enough to include a base for the carry,
    like -99 - 1 = -100 where the list of bases may be [10, 10],
    this function will not try to correct the carry or the -1 in the example

    The list of bases must be greater than or equal to the length of the list of values
    """

    # remove leading zeros
    if a_list[0] == 0:
        a_list = _remove_leading_element(a_list)

    a_list.reverse()
    base_list.reverse()

    for x, (value, base) in enumerate(zip(a_list, base_list)):
        if value >= base or value < 0:
            carry = 0

            if -value >= base:
                value *= -1
                carry = -(value // base)
            else:
                carry = value // base # floor division is necessary

            if x < len(a_list) - 1:
                a_list[x + 1] += carry
            else:
                if value < base:
                    break

                a_list.append(carry)

            a_list[x] = value % base

    a_list.reverse()
    base_list.reverse()

    # removing leading zeros
    if a_list[0] == 0:
        a_list = _remove_leading_element(a_list)

    return a_list


if __name__ == "__main__":
    # here is an example
    print(add([1, 20], [2, 41], [24, 60]))
