# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Class function add

        Adds / appends the value to the DynamicArray
        data structure within the Bag.

        Args:
            value (object): value / object to add within the object
        
        Return:
            None
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        Class function remove

        Removes the value within the given data structure.
        If the value was found and removed it will return True otherwise
        False.

        Args:
            value (object): object value to remove from the data structure

        Return:
            bool if the value was removed successfully
        """
        for i in range(self.size()):
            if self._da.get_at_index(i) == value:
                self._da.remove_at_index(i)
                return True
        return False

    def count(self, value: object) -> int:
        """
        Class function count

        Counts the total number of values that exist within
        the internal data structure

        Args:
            value (object): object value to count

        Returns:
            int of the total number of observations of the value
        """
        arr = self._da.filter(lambda v: v == value)
        return arr.length()

    def clear(self) -> None:
        """
        Class function clear

        Clears the internal data structure overwriting the
        data structure with a new instance of the data structure

        Args:
            None
        
        Return:
            None
        """
        # Simply overwrite the old array with a new empty array
        self._da = DynamicArray()

    def equal(self, second_bag: "Bag") -> bool:
        """
        The method returns True if the bags are equal (contain the same number of
        elements, and also contain the same elements without regard to the order of elements).
        Otherwise, it returns False. An empty bag is only considered equal to another empty bag.
        """
        if self._da.is_empty() and second_bag._da.is_empty():
            return True
        elif self.size() != second_bag.size():
            return False
        else:
            for i in range(self.size()):
                value = self._da.get_at_index(i)
                val_cnt_bag_self = self.count(value)
                val_cnt_bag_other = second_bag.count(value)
                # print(f"First bag count: {val_cnt_bag_self}; Value: {value}")
                # print(f"Second bag count: {val_cnt_bag_other}; Value: {value}")
                if val_cnt_bag_self != val_cnt_bag_other:
                    return False
                
            return True

    def __iter__(self):
        """
        Internal class iterator function to 
        help track internal index
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Internal class iterator incrementor.
        Helps increment the value of the iterator
        and help stop iteration when reached its limit.
        """
        try:
            value = self._da.get_at_index(self._index)
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag4 = Bag([1,2,2])
    bag5 = Bag([2,1,2])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag4.equal(bag5), bag5.equal(bag4))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)
