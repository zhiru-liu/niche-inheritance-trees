import numpy as np
import queue as Q  # queue for ver>3
from functools import total_ordering


@total_ordering
class Node:
    def __init__(self, n=1, r_e=0, R_0=0, born_time=0, parent=None,
                 speciation_time=None, left=None, right=None):
        self.n = n  # niche
        self.r_e = r_e  # boundary
        self.R_0 = R_0  # extrinction parameter
        self.r = self.get_r()  # speciation rate
        self.e = self.get_e()  # extinction rate
        self.left = left  # left node
        self.right = right  # right node
        self.parent = parent  # we can trace back the tree
        self.t2s = None  # time to speciation
        self.born = born_time  # the birth time of this node
        self.spec = self.born + self.get_speciation_time()
        # the speciation_time of the node
        # spec-born = length of the edge
        self.alive = True  # extinct node will be False
        # We don't remove the node in current version
        # below are topological measures
        self.C = None
        self.A = None
        # T is the number of tips, as defined in O Dwyer
        # is_new means that this node is the start of a new species,
        # that is, start counting edge len from this node
        self.T = None
        self.is_new = None

    def __eq__(self, other):
        return self.spec == other.spec

    def __lt__(self, other):
        return self.spec < other.spec

    def get_speciation_time(self):
        '''
        draw a random number according to exponential distribution
        this corresponds to the time that the node speciate
        '''
        if self.get_r() == 0:
            return np.inf
        else:
            return np.random.exponential(1/self.get_r())

    def get_r(self):
        if self.n > 0:
            return self.n
        else:
            return self.r_e

    def get_e(self):
        return self.r/(self.r+self.R_0)

    def speciation(self, mu, sigma, clock):
        '''
        mu and sigma are the parameters for the normal dist
        clock is the global time of the evolutionary process
        clock should be the same as self.spec
        '''
        dn_1 = self.n * np.random.normal(mu, sigma)
        dn_2 = self.n * np.random.normal(mu, sigma)
        n_1 = self.n + dn_1
        n_2 = self.n + dn_2
        self.left = Node(n=n_1, r_e=self.r_e, R_0=self.R_0, born_time=clock,
                         parent=self)
        self.right = Node(n=n_2, r_e=self.r_e, R_0=self.R_0, born_time=clock,
                          parent=self)
        extinction(self.left)
        extinction(self.right)
        return self.left, self.right

    def check_if_new(self):
        # don't call this when self is dead
        if self.parent is None:
            # this is the root node
            return True
        if self.parent.left.alive and self.parent.right.alive:
            # this is a new species
            return True
        elif not self.parent.left.alive and not self.parent.right.alive:
            # Shouldn't happen, since self should be alive
            raise ValueError('Encountered dead node in the list.')
        else:
            return False

    def get_edge_length(self, clock):
        if self.is_new is None:
            raise ValueError('is_new does not exist. Make sure\
                    you get_T first.')
        if not self.is_new:
            # This is not a new species.
            return None
        length = 0
        curr = self
        while True:
            if curr.left is None and curr.right is None:
                # this is a tip
                length += clock - self.born
                return length if curr.spec != np.inf else None
            else:
                if curr.left.alive and curr.right.alive:
                    # the end of this edge
                    length += curr.left.born - curr.born
                    return length
                elif curr.left.alive:
                    # go deeper along this edge
                    length += curr.left.born - curr.born
                    curr = curr.left
                    continue
                elif curr.right.alive:
                    length += curr.right.born - curr.born
                    curr = curr.right
                    continue
                else:
                    # This species went extinct. Shouldn't see it
                    return None

    def get_T(self):
        if self.T:
            return self.T
        else:
            self.is_new = self.check_if_new()
            if self.left is None and self.right is None:
                # this is a tip
                self.T = 1
                return self.T
            left_T = 0
            right_T = 0
            if self.left and self.left.alive:
                left_T = self.left.get_T()
            if self.right and self.right.alive:
                right_T = self.right.get_T()
            self.T = left_T + right_T
            ''' notice that T could be zero, in which case
            the species went extinct
            '''
            return self.T

    def get_A(self):
        if self.A:
            return self.A
        else:
            left_A = 0
            right_A = 0
            if self.left and self.left.alive:
                left_A = self.left.get_A()
            if self.right and self.right.alive:
                right_A = self.right.get_A()
            self.A = left_A + right_A + 1
            return self.A

    def get_C(self):
        if self.C:
            return self.C
        else:
            left_C = 0
            right_C = 0
            if self.left and self.left.alive:
                left_C = self.left.get_C()
            if self.right and self.right.alive:
                right_C = self.right.get_C()
            self.C = left_C + right_C + self.get_A()
            return self.C


class Tree:
    def __init__(self, n=1, r_e=0, R_0=0):
        '''
        R_0 adjusts the extrinction rate
        r_e adjusts the boundary
        n_0 sets the niche of the root node
        '''
        self.root = Node(n, r_e, R_0, born_time=0)
        self.node_list = [self.root]  # in simulte(), root will be added

    def simulate(self, mu, sigma, tree_size):
        '''
        mu and sigma specifies how to inherit the niche
        '''
        # maintain a queue of nodes waiting to speciate
        active_nodes = Q.PriorityQueue()
        active_nodes.put(self.root)
        clock = 0
        size = 1
        # each step, take an element and process
        while size < tree_size:
            if not active_nodes.empty():
                curr = active_nodes.get()
                clock = curr.spec  # forward time to spec time
                if not curr.alive:
                    continue
                # give birth to two nodes at clock time
                left, right = curr.speciation(mu, sigma, clock)
                if left.alive:
                    if left.spec != np.inf:
                        active_nodes.put(left)
                    self.node_list.append(left)
                    size += 1
                if right.alive:
                    if right.spec != np.inf:
                        active_nodes.put(right)
                    self.node_list.append(right)
                    size += 1
            else:
                print('The system went extinct at size %d, please\
                        try again or adjust the parameters' % size)
                return active_nodes, clock
        return active_nodes, clock

    def get_AC_list(self):
        lst = []
        for node in reversed(self.node_list):
            lst.append(np.array([node.get_A(), node.get_C()]))
        return np.array(lst)

    def get_EAD(self, clock):
        lst = []
        for node in reversed(self.node_list):
            # this pass, calculate all the T and is_new
            node.get_T()
        for node in reversed(self.node_list):
            length = node.get_edge_length(clock)
            if length:
                lst.append(np.array([node.get_T(), length]))
        return np.array(lst)

    def get_specs(self):
        result = []
        for node in self.node_list:
            result.append(node.spec)
        return np.array(result)


def extinction(x):
    # x should be a Node object
    if x.get_e() > np.random.uniform():
        x.alive = False
    return
