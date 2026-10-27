# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        class function insert_front

        Inserts a Node object at the front of the Linked List

        Args:
            value (object): value to insert into Node Object to insert at the LinkedList

        Return:
            None
        """
        # If we have a node after Sentinel, then insert at front
        if not self.is_empty():
            # Copy previous next value of sentinel node
            curr_sent_next = self._head.next
            # overwrite the sentinel node next value with new node insert
            self._head.next = SLNode(value=value)
            # Point the previous next value to the new insertion
            self._head.next.next = curr_sent_next
            return
        # Otherwise the LinkedList is empty and insert new node at head
        else:
            self._head.next = SLNode(value=value)
            return

    def insert_back(self, value: object) -> None:
        """
        class function insert_back

        Inserts a Node object at the back of the Linked List

        Args:
            value (object): value to insert into Node Object to insert at the LinkedList

        Return:
            None
        """
        curr_node = self._head
        if curr_node:
            prev_node = None
            while curr_node:
                prev_node = curr_node
                curr_node = curr_node.next
            prev_node.next = SLNode(value=value)
        else:
            self._head.next = SLNode(value=value)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        class function insert_at_index

        Inserts the value at the corresponding index number
        related to the number of nodes in the Linked List.

        Args:
            index (int): index in which to insert the value
            value (object): value to create Node for which to insert at the index

        Return:
            None
        """
        if index < 0 or index > self.length():
            raise SLLException
        
        curr_node = self._head # Sentinel node
        # Create new node to insert
        new_node = SLNode(value=value)
        # Loop to the correct node
        for i in range(index):
            curr_node = curr_node.next
        # point new node next to previous current nodes next
        new_node.next = curr_node.next
        # point current node next to new node
        curr_node.next = new_node
        

    def remove_at_index(self, index: int) -> None:
        """
        class function remove_at_index
        
        Remove the value at the corresponding index number
        related to the number of nodes in the Linked List.

        Args:
            index (int): index in which to remove the value

        Return:
            None
        """
        if index < 0 or index >= self.length() or self.is_empty():
            raise SLLException
        
        curr_node = self._head
        if index == 0:
            curr_node.next = curr_node.next.next
        else:
            prev_node = curr_node
            for i in range(index):
                prev_node = curr_node
                curr_node = curr_node.next
            # Overwrite the current node to remove the node at the index
            # We overwrite the value with the next node we want to remove
            # with it's next pointer
            curr_node.next = curr_node.next.next

    def remove(self, value: object) -> bool:
        """
        class function remove

        function removes the value corresponding
        to the Node for which it exists in the LinkedList.
        If the value / Node exists, then the function will return True
        to indicate the Node has been removed successfully, else False.

        Args:
            value (object): value to remove from LinkedList

        Return
            bool to indicate if the value was removed 
        """
        curr_node = self._head
        prev_node = curr_node
        while curr_node and curr_node.value != value:
            # Remember the previous node
            prev_node = curr_node
            # Update the current mode
            curr_node = curr_node.next
        # If we stil have a Node at the end of traversal
        if curr_node:
            prev_node.next = curr_node.next
            return True
        else:
            return False

    def count(self, value: object) -> int:
        """
        class function count

        counts the total Nodes for which the value exists in

        Args:
            value (object): value to count within the LinkedList

        Return:
            int of the total count of the object
        """
        counter = 0
        curr_node = self._head
        while curr_node:
            if curr_node.value == value:
                counter += 1
            # Update the current mode
            curr_node = curr_node.next

        return counter

    def find(self, value: object) -> bool:
        """
        class function find

        finds the value within the LinkedList if it exists

        Args:
            value (object): object to search for within the LinkedList

        Returns:
            bool if whether the object was found in the LinkedList
        """
        curr_node = self._head
        found = False
        while curr_node and not found:
            if curr_node.value == value:
                found = True
                return found
            else:
                curr_node = curr_node.next

        return found

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        class function slice

        slices the LinkedList nodes / values within the LinkedList
        based on the start index and size.

        Args:
            start_index (int): starting index value to begin slicing from
            size (int): total values to slice

        Return:
            LinkedList of the sliced Nodes / values
        """

        end_ix = start_index + size - 1
        # length = 10
        # start = 10
        # size = 0
        # end = 10 + 0 - 1 = 9
        if start_index < 0 or (end_ix) >= self.length() or size < 0 or self.is_empty() or start_index >= self.length():
            raise SLLException
        # Track when we reach the start index
        _iter = 0
        # Init curr node tracker
        curr_node = self._head
        # Tracker to know when we're slicing still
        slicing = True
        # Build end index based on size
        
        # Linked List to export
        ll = LinkedList()
        # Beginning going through the list to find when we start 
        while curr_node and slicing:
            # iterate to next node
            curr_node = curr_node.next
            # Check if we're in the range of slicing and inserting the value into new LinkedList
            if _iter >= start_index and _iter <= end_ix:
                ll.insert_back(curr_node.value)
            elif _iter > end_ix:
                slicing = False
            _iter += 1

        return ll
            

        


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_cases = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_cases:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_cases = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_cases:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")
