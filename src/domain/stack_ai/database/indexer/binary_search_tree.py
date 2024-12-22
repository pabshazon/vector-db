class Node:
    def __init__(self, key, value):
        self.key   = key
        self.value = value
        self.left  = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def add_node(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            parent_node = self._choose_parent_node(self.root, key)
            side        = self._choose_left_or_right(parent_node, key)

            if side == "left":
                if parent_node.left is None:
                    parent_node.left = Node(key, value)
                else:
                    parent_node.left.value = value

            elif side == "right":  # @todo finish - continue from here after plane.


    def _choose_parent_node(self, orphan_node, key):

    def _choose_left_or_right(self, parent_node, key):

    def insert
    def update
    def read
    def delete
