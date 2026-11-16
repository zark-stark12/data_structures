# Name: Juan Zarco
# OSU Email: zarcoj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: # 4
# Due Date: 11/16/2026
# Description: 


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """AVL Tree class. Inherits from BST"""

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ---------------------------------------------------------------------- #

    def add(self, value: object) -> None:
        """
        class function add

        Function adds the value object into the AVL tree within the AVL node
        that contains the parent and height parameter on top
        of the existing Binary search tree node object.

        Args:
            value (object): value to add to the AVL tree

        Return:
            None
        """
        if self.is_empty():
            self._root = AVLNode(value)
        else:
            traversing = True
            node = self.get_root()
            # Let's use a while loop to tranverse the tree
            while traversing:
                # If the input value is greater than or equal to node value
                # Input new node as right leaft
                if value == node.value:
                    # Return if duplicate value was found to ensure no duplicates are added
                    return
                elif value >= node.value:
                    if node.right:
                        node = node.right
                    else:
                        new_node = AVLNode(value)
                        node.right = new_node
                        new_node.parent = node
                        self._rebalance(new_node)
                        traversing = False
                else:
                    if node.left:
                        node = node.left
                    else:
                        new_node = AVLNode(value)
                        node.left = new_node
                        new_node.parent = node
                        self._rebalance(new_node)
                        traversing = False
            
            

    def remove(self, value: object) -> bool:
        """
        class function remove

        Finds and removes the value from the AVL tree if the value was found

        Args:
            value (object): value to remove from the AVL tree

        Return:
            bool if the object was found and removed
        """
        if self.is_empty():
            return False
        else:
            # get the starting root to iterate through for removal
            node = self.get_root()
            parent = None
            # Find the node to remove
            while node and node.value != value:
                parent = node
                if value >= node.value:
                    node = node.right
                else:
                    node = node.left
            # couldn't find the node to remove!
            if node is None:
                return False
            
            if node.left and node.right:
                # get the successor parent to rebalance the tree on after removal
                # this sets the rebalancing point based on the successors parent
                rebalanced = self._remove_two_subtrees(parent, node)
            else:
                # the nodes parent is the pivot point to begin rebalancing
                rebalanced = node.parent
                # finding the sub leaf of the parent
                leaf = node.left if node.left else node.right

                if leaf:
                    leaf.parent = node.parent
                # Handle the root removal case
                if node.parent is None:
                    self._root = leaf
                elif node is node.parent.left:
                    node.parent.left = leaf
                else:
                    node.parent.right = leaf
            # Rebalance the AVL tree after removal
            if rebalanced:
                self._rebalance(rebalanced)

            return True


    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        private helper class function to remove the node that has two exisiting leaf nodes under it
        """
        # first go right init the successor
        successor = remove_node.right
        # init the successor parent as the remove node
        successor_parent = remove_node
        # Continue left to get the next successor to replace the remove node
        while successor.left:
            successor_parent = successor
            successor = successor.left
        # point the value of the remove node to the successors value
        remove_node.value = successor.value
        # if there's a successor right, point it to the leaf above it previously to it's right
        if successor.right is not None:
            successor.right.parent = successor_parent
        # Same thing but with the left but point successor's right to it's left
        if successor is successor_parent.left:
            successor_parent.left = successor.right
        else:
            successor_parent.right = successor.right
        # return the successor parent to help rebalance the AVL tree
        return successor_parent

    def _balance_factor(self, node: AVLNode) -> int:
        """
        private helper function to calculate the balance factor of a node / leaf
        """
        return self._get_height(node.right) - self._get_height(node.left)

    def _get_height(self, node: AVLNode) -> int:
        """
        private helper function to retrieve the heigh of a node / leaf
        """
        return node.height if node else -1

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        private helper function to rotate the avl tree nodes left to balance
        """
        # Since we're rotating left, start from the right of the node to move left
        root = node.right
        node.right = root.left
        if root.left:
            root.left.parent = node

        root.parent = node.parent
        if node.parent is None:
            self._root = root
        elif node is node.parent.left:
            node.parent.left = root
        else:
            node.parent.right = root

        root.left = node
        node.parent = root

        self._update_height(node)
        self._update_height(root)
        return root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        private helper function to rotate the avl tree nodes right to balance
        """
        # rotating right thus we need to reference the new root coming from the left
        root = node.left
        node.left = root.right
        if root.right:
            root.right.parent = node
        # update parent pointers
        root.parent = node.parent
        if node.parent is None:
            self._root = root
        elif node is node.parent.right:
            node.parent.right = root
        else:
            node.parent.left = root

        root.right = node
        node.parent = root

        self._update_height(node)
        self._update_height(root)
        return root

    def _update_height(self, node: AVLNode) -> None:
        """
        private helper function to help update the height of the AVL node / leaf
        """
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        node.height = (1 + left_height) if left_height > right_height else (1 + right_height)

    def _rebalance(self, node: AVLNode) -> None:
        """
        private helper function to help rebalance the AVL tree utilizing other helper functions derived.

        The function helpers update heights and calculates balance factors while rotating based on the 
        current balance factor.
        """
        while node:
            self._update_height(node)
            curr_balance = self._balance_factor(node)
            # If we're left heavy, need to rotate right
            if curr_balance < -1:
                if self._balance_factor(node.left) > 0:
                    self._rotate_left(node.left)
                node = self._rotate_right(node)
            # if we're right heavy, rotate left
            elif curr_balance > 1:
                if self._balance_factor(node.right) < 0:
                    self._rotate_right(node.right)
                node = self._rotate_left(node)

            node = node.parent

            


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
