import numpy as np
import queue as Q  # queue for ver>3
from functools import total_ordering


@total_ordering
class Node:
    def __init__(self, born_time=0, parent=None,
                 left=None, right=None):
        self.left = left  # left node
        self.right = right  # right node
        self.parent = parent  # we can trace back the tree
        self.born = born_time  # the birth time of this node
        self.length = self.get_interval()
        # the speciation_time of the node
        self.visible = False
        self.C = None
        self.A = None
        # T is the number of tips, as defined in O Dwyer
        self.T = None

    def __eq__(self, other):
        return self.born + self.length == other.born + other.length

    def __lt__(self, other):
        return self.born + self.length < other.born + other.length

    def get_interval(self):
        return np.random.exponential(1)

    def speciation(self, clock):
        self.left = Node(born_time=clock, parent=self)
        self.right = Node(born_time=clock, parent=self)
        return self.left, self.right

    def get_T(self):
        if self.T:
            return self.T
        else:
            if self.left is None and self.right is None:
                # this is a tip
                self.T = 1
                return self.T
            left_T = 0
            right_T = 0
            if self.left:
                left_T = self.left.get_T()
            if self.right:
                right_T = self.right.get_T()
            self.T = left_T + right_T
            return self.T

    def get_A(self):
        if self.A:
            return self.A
        else:
            left_A = 0
            right_A = 0
            if self.left:
                left_A = self.left.get_A()
            if self.right:
                right_A = self.right.get_A()
            self.A = left_A + right_A + 1
            return self.A

    def get_C(self):
        if self.C:
            return self.C
        else:
            left_C = 0
            right_C = 0
            if self.left:
                left_C = self.left.get_C()
            if self.right:
                right_C = self.right.get_C()
            self.C = left_C + right_C + self.get_A()
            return self.C

    def to_string(self, clock):
        if self.left is None and self.right is None:
            return ':' + str(clock-self.born)
        else:
            leftStr = self.left.to_string(clock)
            rightStr = self.right.to_string(clock)
            return '(' + leftStr + ',' + rightStr + ')' \
                       + ':' + str(self.length)

    def prune(self):
        if not self.visible:
            raise ValueError('Calling prune on invisible node')
        curr = self
        while True:
            if curr.left is None and curr.right is None:
                self.length = curr.born + curr.length - self.born
                self.left = None
                self.right = None
                return

            if curr.left.visible and curr.right.visible:
                # reaching the speciation point
                self.spec = curr.born + curr.length - self.born
                self.left = curr.left
                self.right = curr.right
                self.left.prune()
                self.right.prune()
                return

            if curr.left.visible:
                curr = curr.left
                continue
            elif curr.right.visible:
                curr = curr.right
                continue


class Tree:
    def __init__(self, speciation_prob=0.5):
        self.root = Node()
        self.speciation_prob = speciation_prob
        self.node_list = [self.root]

    def simulate(self, tree_size):
        # maintain a queue of nodes waiting to speciate
        active_nodes = Q.PriorityQueue()
        active_nodes.put(self.root)
        clock = 0
        size = 1
        while size < tree_size:
            if not active_nodes.empty():
                curr = active_nodes.get()
                clock = curr.born + curr.length
                ''' this is the dead later version '''
                if np.random.rand() < self.speciation_prob:
                    # success
                    left, right = curr.speciation(clock)
                    active_nodes.put(left)
                    active_nodes.put(right)
                    self.node_list.append(left)
                    self.node_list.append(right)
                    size += 2
            else:
                return False, size
        self.trace_back(active_nodes)  # mark nodes as visible
        return True, clock

    def trace_back(self, queue):
        while not queue.empty():
            curr = queue.get()
            curr.visible = True
            while curr.parent is not None:
                if curr.parent.visible:
                    break
                else:
                    curr.parent.visible = True
                    curr = curr.parent
        return

    def prune_tree(self):
        self.root.prune()

    def get_AC_list(self):
        lst = []
        for node in reversed(self.node_list):
            lst.append(np.array([node.get_A(), node.get_C()]))
        return np.array(lst)
