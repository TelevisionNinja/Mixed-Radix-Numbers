def _pad_left(arr, padding_element, length):
    for _ in range(length - len(arr)):
        arr.insert(0, padding_element)


def _remove_leading_element(arr):
    if arr:
        while arr[0] == 0:
            del arr[0]

            if not arr:
                arr = [0]
                break
    return arr


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


def _make_lists_equal_length(list_1, list_2, base_bool):
    length_1 = len(list_1)
    length_2 = len(list_2)

    if length_1 != length_2:
        max_len = max(length_1, length_2)

        _pad_left(list_1, 0, max_len)

        if base_bool:
            _pad_left(list_2, list_2[0], max_len)
        else:
            _pad_left(list_2, 0, max_len)


def _make_whole_list_negative(a_list):
    for x in range(len(a_list)):
        if a_list[x] > 0:
            a_list[x] *= -1
    return a_list


def _format_into_regular_negative_number(a_list):
    for x in range(len(a_list)):
        if a_list[x] < 0:
            a_list[x] *= -1
    a_list[0] *= -1
    return a_list


def _check_if_negative(a_list):
    if a_list[0] < 0:
        a_list = _make_whole_list_negative(a_list)
    return a_list


def _formate_numbers(num_list_1, num_list_2):
    num_list_1 = _check_if_negative(num_list_1)
    num_list_2 = _check_if_negative(num_list_2)
    
    _make_lists_equal_length(num_list_1, num_list_2, False)


def add(num_arr_1, num_arr_2, base_arr):
    """
    num_arr_1 + num_arr_2
    """
    
    _formate_numbers(num_arr_1, num_arr_2)
    
    return clean_up_bases([x + y for x, y in zip(num_arr_1, num_arr_2)], base_arr)


def subtract(num_arr_1, num_arr_2, base_arr):
    """
    num_arr_1 - num_arr_2
    """

    _formate_numbers(num_arr_1, num_arr_2)

    negative_flag = _compare_numbers_represented_as_arrays(num_arr_1, num_arr_2)

    if negative_flag == -1:
        num_arr_1, num_arr_2 = num_arr_2, num_arr_1

    result = clean_up_bases([x - y for x, y in zip(num_arr_1, num_arr_2)], base_arr)

    if negative_flag == -1 and result[0] > 0:
        result[0] *= -1

    return result


def clean_up_bases(arr, base_arr):
    arr = clean_up_bases_ignore_most_significant_digit(arr, base_arr)

    # test for length
    # this deals with the most significant digit if it is greater than or euqal to or less than or equal to the negative of the base
    
    if len(arr) > len(base_arr):
        while arr[0] >= base_arr[0] or -arr[0] >= base_arr[0]:
            carry = 0

            if -arr[0] >= base_arr[0]:
                arr[0] *= -1
                carry = -(arr[0] // base_arr[0])
            else:
                carry = arr[0] // base_arr[0]
            
            arr.insert(0, carry)
            arr[1] = arr[1] % base_arr[0]

    return arr


def clean_up_bases_ignore_most_significant_digit(arr, base_arr):
    if arr[0] == 0:
        arr = _remove_leading_element(arr)

    for x in arr:
        if x > 0:
            break
    else:
        arr = _format_into_regular_negative_number(arr)

    arr.reverse()
    base_arr.reverse()

    for x, (value, base) in enumerate(zip(arr, base_arr)):
        if value >= base or value < 0:
            carry = 0
            if -value >= base:
                value *= -1
                carry = -(value // base)
            else:
                carry = value // base # floor division
            
            if x < len(arr) - 1:
                arr[x + 1] += carry
            else:
                if value < base:
                    break
                arr.append(carry)
            arr[x] = value % base

    arr.reverse()
    base_arr.reverse()

    # removing leading zeros that may show up
    if arr[0] == 0:
        arr = _remove_leading_element(arr)

    return arr
