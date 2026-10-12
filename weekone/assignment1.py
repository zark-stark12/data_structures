# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


import random
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------


def min_max(arr: StaticArray) -> tuple[int, int]:
    """
    Min - Max function method around StaticArray.

    Function calculates the minimum and maximum value of the Static Array.

    Args:
        arr (StaticArray): StaticArray of integer values

    Returns:
        tuple[int, int]: min, max of the array of integers
    """
    max = arr.get(0)
    min = arr.get(0)
    for i in range(arr.length()):
        val = arr.get(i)
        max = val if val > max else max
        min = val if val < min else min

    return min, max



# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------


def fizz_buzz(arr: StaticArray) -> StaticArray:
    """
    Fizz Buzz Function writer

    Function writes fizz, buzz or fizzbuzz based on the following rules:
    - "fizzbuzz" if the integer value is divisible by both 5 and 3.
    - "fizz" if the integer value is divisible by only 3
    - "buzz" if the integer value is divisible by only 5

    Args:
        arr (StaticArray): StaticArray of integer values
    
    Returns:
        StaticArray of values written with fizz, buzz, or fizzbuzz with other integer values untouched.

    """
    fizzbuzz_arr = StaticArray(arr.length())
    for i in range(arr.length()):
        val = arr.get(i)
        if val % 5 == 0 and val % 3 == 0:
            fizzbuzz_arr.set(i, "fizzbuzz")
        elif val % 3 == 0:
            fizzbuzz_arr.set(i, "fizz")
        elif val % 5 == 0:
            fizzbuzz_arr.set(i, "buzz")
        else:
            fizzbuzz_arr.set(i, val)

    return fizzbuzz_arr



# ------------------- PROBLEM 3 - REVERSE -----------------------------------


def reverse(arr: StaticArray) -> None:
    """
    StaticArray Reverser

    Function takes the StaticArray and reverses the array values in-place.

    Args:
        arr (StaticArray): StaticArray of object data type values

    Returns:
        None
    """
    l = arr.length()
    midpoint = l // 2
    for i in range(midpoint):
        temp = arr.get(l - i - 1)
        arr.set(l - i - 1, arr.get(i))
        arr.set(i, temp)
    


# ------------------- PROBLEM 4 - ROTATE ------------------------------------


def rotate(arr: StaticArray, steps: int) -> StaticArray:
    """
    StaticArray rotater

    The function takes a static array and "rotates" or simply shifts the values of the
    array in a given direction based on the integer steps.

    Args:
        arr (StaticArray): StaticArray of object values to rotate or shift
        steps (int): The direction for rotating the values within the StaticArray along
        with how many steps.

    Returns:
        StaticArray with values that have been rotated / shifted
    """
    l = arr.length()
    arr_copy = StaticArray(size=l)
    for i in range(l):
        ix = (i + steps) % l
        arr_copy.set(ix, arr.get(i))
    return arr_copy
    


# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------


def sa_range(start: int, end: int) -> StaticArray:
    """
    Static Array generator for range of values

    Args:
        start (int): starting point of the StaticArray
        end (int): end point of the StaticArray

    Returns:
        StaticArray of integer values from the start and end range.
    """
    # Handle cases where difference is negative or zero
    size_diff = end - start
    if size_diff == 0:
        arr_size = 1
    elif size_diff > 0:
        arr_size = size_diff + 1
    elif size_diff < 0:
        arr_size = (-1 * size_diff) + 1
    
    arr = StaticArray(arr_size)
    end_point = end + 1 if start <= end else end - 1
    step = 1 if start <= end else -1
    for ix, val in enumerate(range(start, end_point, step)):
        arr.set(ix, val)

    return arr


# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------


def is_sorted(arr: StaticArray) -> int:
    """
    StaticArray sorter check

    Args:
        arr (StaticArray): StaticArray of integer values

    Returns:
        - 1 if the array is strictly monotonically increasing
        - -1 if the array is strictly monotonically decreasing
        - 0 if the array is neither strictly increasing nor decreasing
    
    """
    # Using transitive property to apply monotonically increasing or decreasing 
    # sequences
    # Preserve memory if we found values increasing and decreasing
    # If both are 1 then this should exit and return 0
    increasing_flag = None
    decreasing_flag = None
    # base case to return
    if arr.length() == 1:
        return 1

    for i in range(arr.length()-1):
        if arr.get(i) < arr.get(i + 1):
            increasing_flag = 1
        elif arr.get(i) > arr.get(i + 1):
            decreasing_flag = 1
        elif arr.get(i) == arr.get(i + 1):
            # Break here since we found non strictly increasing or decreasing
            return 0

        if increasing_flag and decreasing_flag:
            # Break here since we found non strictly increasing or decreasing
            return 0
    return 1 if increasing_flag else -1

# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------


def find_mode(arr: StaticArray) -> tuple[object, int]:
    """
    Find Mode Function

    The function is used to find the statistical mode of the StaticArray.
    The array must be in either ascending or descending order for the assumption.

    Args:
        arr (StaticArray): StaticArray of object values

    Returns:
        tuple[object, int] => the mode of StaticArray, integer frequency of appearances in the StaticArray
    """
    # initialize mode and frequency
    mode = arr.get(0)
    frequency = 1
    arr_len = arr.length()
    # Intialize tracker for looping
    tracking_val = mode
    tracking_count = frequency
    # Since the assumption is the data is already sorted
    # We can track the count of the values as we're looping through it
    for i in range(1, arr_len):
        new_val = arr.get(i)

        if new_val == tracking_val:
            tracking_count += 1
        else:
            # If we find a new value, update the tracker
            tracking_val = new_val
            tracking_count = 1
        # If the new value found has a larger frequency
        # then we updat the mode and frequency
        if tracking_count > frequency:
            mode, frequency = tracking_val, tracking_count
       
    return mode, frequency



# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------


def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    StaticArray Duplicate remover

    Removes duplicate values found in the StaticArray
    and returns a new StaticArray of dedupped values.

    Args:
        arr (StaticArray): StaticArray of object values

    Returns:
        StaticArray of dedupped values
    """
    l = arr.length()
    # Distinct value tracker
    distinct_values = 1
    # Initialize dedupped array for export
    arr_tracker = StaticArray(l)
    arr_tracker.set(0, arr.get(0))
    # Initialize distinct counter
    d = 1
    # O(n)
    for i in range(1, l):
        # Get next value in the array
        new_val = arr.get(i)
        # If it's new to the previous value
        # Add it to the arr
        if new_val != arr_tracker.get(d-1):
            arr_tracker.set(d, new_val)
            # Increment distinct counter
            d += 1

    # Generate the dedupped array
    # Looping over d times  => d + n < 2n
    arr_export = StaticArray(d)
    for k in range(d):
        arr_export.set(k, arr_tracker.get(k))

    return arr_export
        


# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------


def count_sort(arr: StaticArray) -> StaticArray:
    """
    Count Sort algorithm (descending) implementation
    
    The count_sort function takes a StaticArray and returns
    a new StaticArray of the original values in descending order.

    Args:
        arr (StaticArray): StaticArray of integer values

    Returns:
        StaticArray of integer values in descending order
    """
    arr_len = arr.length()
    num_tracker = StaticArray(arr_len)
    num_tracker.set(0, arr.get(0))
    min, max = min_max(arr)
    if min > 0:
        min = 0
    # initialize k range
    k = max - min + 1
    # Initialize the counter for each unique value in the range
    counter = StaticArray(k)
    for j in range(k):
        counter.set(j, 0)

    # Look through each value in the array and count them
    # [100, 34, 12, 10, -5]
    # max = 100
    # min = -5
    # idx = 100 - (-5)
    # idx = 105
    for i in range(arr_len):
        # Get idx, if min is negative
        # Idx is offset by the negative value
        idx = arr.get(i) - min
        # Set the count for the value in the counter plus 1
        counter.set(idx, counter.get(idx) + 1)
    # Cumulative counts (descending order)
    for k in range(k - 2, -1, -1):
        counter.set(k, counter.get(k) + counter.get(k + 1))
    # Now we apply the sorting
    count_sorted_arr = StaticArray(arr_len)
    for i in range(arr_len - 1, -1, -1):
        val = arr.get(i)
        count_idx = val - min
        # decreasing the count
        counter.set(count_idx, counter.get(count_idx) - 1)
        count_sorted_arr.set(counter.get(count_idx), val)
    return count_sorted_arr


# ------------------- PROBLEM 10 - SORTED SQUARES ---------------------------


def sorted_squares(arr: StaticArray) -> StaticArray:
    """
    StaticArray sorter of squared values

    sorted_squares takes the original array and applies the power of 2
    or squares the integer value and sort the array in non-descending order.

    This assumes the original array is already sorted in ascending order.

    Args:
        arr (StaticArray): StaticArray of integer values

    Returns:
        StaticArray of squared values sorted in ascending order.
    """
    arr_len = arr.length()
    square_array = StaticArray(arr_len)
    # Compare values on both ends and iterate when finding a higher value
    # Update the index value higher or lower depending if the value found is
    # higher than the value on the other side.
    left_idx = 0
    right_idx = arr_len - 1
    for ix in range(arr_len - 1, -1, -1):
        if (arr.get(left_idx) ** 2) < (arr.get(right_idx) ** 2):
            square_array.set(ix, arr.get(right_idx) ** 2)
            right_idx -= 1
        else:
            square_array.set(ix, arr.get(left_idx) ** 2)
            left_idx += 1

    return square_array


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]: 3}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        result = min_max(arr)
        if result:
            print(f"Min: {result[0]: 3}, Max: {result[1]}")
        else:
            print("min_max() not yet implemented")

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-95, -89), (-89, -95)]
    for start, end in cases:
        print(f"Start: {start: 4}, End: {end: 4}, {sa_range(start, end)}")

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = is_sorted(arr)
        space = "  " if result is not None and result >= 0 else " "
        print(f"Result:{space}{result}, {arr}")

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value

        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(f"Before: {arr}")
        result = count_sort(arr)
        print(f"After : {result}")

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-10 ** 9, 10 ** 9 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')
