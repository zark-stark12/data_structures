# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Class function: resize

        Resizes the given array to new capacity.
        Capacity must be a positive number and cannot be lower
        than the current total elements stored in the array.

        Args:
            new_capacity (int): value to adjust the limit of the Dynamic Array

        Return:
            None
        """
        if new_capacity < self.length() or new_capacity == 0:
            return
        else:
            temp = StaticArray(new_capacity)
            # initial_length = self.length()
            for ix in range(new_capacity):
                if ix > self.length() - 1:
                    temp.set(ix, None)
                else:
                    temp.set(ix, self.get_at_index(ix))
            self._data = temp
            self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        Class method append

        Appends element to the DynamicArray.
        If the DynamicArray is at max capacity, the capacity
        is resized to double it's current capacity.

        Args:
            value (object): value / element to append within the array

        Return:
            None
        """
        # Check if we're at max capacity
        if self.get_capacity() == self.length():
            self.resize(self.get_capacity() * 2)
            # New index to append should be the end of the size
            ix = self.length()
            self._data.set(ix, value=value)
            # Update size
            self._size += 1
        else:
            # New index to append should be the end of the size
            ix = self.length()
            self._data.set(ix, value=value)
            # Update size
            self._size += 1


    def insert_at_index(self, index: int, value: object) -> None:
        """
        Class method insert_at_index

        Inserts value at specified index.

        If a value is at the index specified, values
        are shifted right within the array to make room
        for the new value.

        Index must be a valid index between [0, N-1]
        where N is the total elements.

        Args:
            index (int): position to insert
            value (object): value to insert
        
        Return:
            None

        """
        if index < 0 or index > self.length():
            raise DynamicArrayException
        # Let's check first if there is any value at the specified index
        if self.get_capacity() == self.length():
            self.resize(self.get_capacity() * 2)
        elif index + 1 > self.get_capacity():
            self.resize(self.get_capacity() * 2)
        if self._data.get(index):
            # Increment to the total size, not the total array to update
            for i in range(self.length() - 1, index - 1, -1):
                curr_val_at_ix = self.get_at_index(i)
                # self.set_at_index(index=i+1, value=curr_val_at_ix)
                self._data.set(index=i+1, value=curr_val_at_ix)
            # Finally now that we shifted the values up we can set the value at the index
            # with the new value
            self.set_at_index(index=index, value=value)
            # Since we always shift the values and never delete
            # Need to increment the size
            self._size += 1
        else:
            # If the index is None, update the value there.
            self._data.set(index=index, value=value)
            self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Class method remove_at_index
        
        Removes value at specified index.

        Value is removed at the specified index by shifting values
        of the array to overwrite the current position.

        If the total number of elements is smaller than the 
        capacity / 4, we then resized in half.

        The DynamicArray cannot be resized if the array capacity
        is 10 or below.

        Args:
            index (int): position to remove value
        
        Return:
            None
        """
        min_capacity_limit = 10
        # Capacity check
        # Comment to check the examples since examples are < 10 capacity
        # if self.get_capacity() <= min_capacity_limit:
        #     return
        if index > self.length() - 1 or index < 0:
            raise DynamicArrayException
        # Check for size vs capacity ratio and ensure we are not resizing below 10
        # We cannot reduce below 10 thus we apply this additional check
        if self.length() < (self.get_capacity()/4):
            # print("Uh oh we're here for capacity: ", self.get_capacity())
            # print("What's twice the length? ", self.length() * 2)
            if self.get_capacity() > min_capacity_limit and self.length() * 2 < min_capacity_limit:
                self.resize(min_capacity_limit)
            elif self.get_capacity() > min_capacity_limit and self.length() * 2 > min_capacity_limit:
                self.resize(self.length() * 2)
        # Main goal is to shift all the elements to overwrite / remove the element at the index
        # We start at the index and look at the value to the right
        
        for i in range(index, self.length() - 1):
            self.set_at_index(index=i, value=self._data.get(i + 1))
        self.set_at_index(self.length() - 1, None)
        self._size -= 1


    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Class function slice

        The function returns a DynamicArray of the array values between
        the start index and total size.

        The start_index and start_index + size must be between
        [0, N-1] where N is the total elements.

        Args:
            start_index (int): beginning index to slice from
            size (int): total elements to slice
        
        Returns:
            DynamicArray of the sliced values
        """
        if start_index < 0 or start_index > self.length() - 1:
            raise DynamicArrayException
        elif size > self.length() or start_index + size > self.length() or size < 0:
            raise DynamicArrayException

        arr = DynamicArray()
        for i in range(start_index, start_index + size):
            arr.append(self.get_at_index(i))
        return arr


    def merge(self, second_da: "DynamicArray") -> None:
        """
        Class method merge

        Merges the values of the DynamicArry into the current 
        array.

        Args:
            seconda_da (DynamicArray): the DynamicArray to merge the values

        Return:
            None
        """
        for j in range(second_da.length()):
            self.append(second_da.get_at_index(j))

    def map(self, map_func) -> "DynamicArray":
        """
        Class method map

        Class method to apply the mapping function 
        at each value within the Dynamic Array.

        Args:
            map_func: Python function to map against the values

        Return:
            DynamicArray with the values applied from the map_func

        """
        arr = DynamicArray()
        for i in range(self.length()):
            arr.append(map_func(self.get_at_index(i)))

        return arr

    def filter(self, filter_func) -> "DynamicArray":
        """
        Class method filter

        The function helps apply the filter function
        to the values of the array if it passes the filter function
        which should return a boolean value.

        Args:
            filter_func: Python function that returns a boolean
        
        Return:
            DynamicArray of the values that returned True from the filter_func
        """
        arr = DynamicArray()
        for i in range(self.length()):
            if filter_func(self.get_at_index(i)):
                arr.append(self.get_at_index(i))

        return arr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Class method reduce

        Function applies the reduce_func to help reduce 
        and merge the values of the array from the reduce_func
        itself.

        Args:
            reduce_func: Python function to apply the reduction
            initiliazer: Optional value to help apply the first value for the reduce_func

        Return:
            object value as a result of the reduce_func
        """
        head = None
        if self.is_empty():
            return initializer

        if self.length() == 1 and initializer:
            return reduce_func(initializer, self.get_at_index(0))
        elif self.length() == 1:
            return self.get_at_index(0)
        
        if initializer:
            head = reduce_func(initializer, self.get_at_index(0))
            for i in range(1, self.length()):
                head = reduce_func(head, self.get_at_index(i))
        else:
            head = reduce_func(self.get_at_index(0), self.get_at_index(1))
            for i in range(2, self.length()):
                head = reduce_func(head, self.get_at_index(i))
        return head

def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    find_mode

    Using similar construction as from week one for mode and frequency
    """
    # initialize mode and frequency
    mode = arr.get_at_index(0)
    frequency = 1
    arr_len = arr.length()
    # Intialize tracker for looping
    tracking_val = mode
    tracking_count = frequency

    mode_arr = DynamicArray()
    mode_arr.append(mode)
    for i in range(1, arr_len):
        new_value = arr.get_at_index(i)
        if new_value == tracking_val:
            tracking_count += 1
        else:
            tracking_val = new_value
            tracking_count = 1

        if tracking_count == frequency:
            mode_arr.append(tracking_val)
            mode, frequency = tracking_val, tracking_count
        elif tracking_count > frequency:
            # New frequency found overwrite old array and append new value
            mode_arr = DynamicArray()
            mode_arr.append(tracking_val)
            # Update frequency / tracking count
            mode, frequency = tracking_val, tracking_count

    return mode_arr, frequency


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))


    print("\n# find_mode example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
