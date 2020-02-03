import numpy as np
import queue as Q  # queue for ver>3
from functools import total_ordering


@total_ordering
class Node:
    def __init__(self, n=1, r_e=0, R_0=0, born_time=0, parent=None,
                 speciation_time=None, left=None, right=None, index=0):
        self.n = n  # niche
        self.r_e = r_e  # boundary
        self.R_0 = R_0  # extrinction parameter
        self.r = self.get_r()  # speciation rate
        self.e = self.get_e()  # extinction rate
        self.left = left  # left node
        self.right = right  # right node
        self.parent = parent  # we can trace back the tree
        self.born = born_time  # the birth time of this node
        self.spec = self.born + self.get_speciation_time()
        # the speciation_time of the node
        # spec-born = length of the edge
        self.alive = True  # extinct node will be False
        self.visible = False  # whether this node is \
        # visible when traced back
        # We don't remove the node in current version
        # below are topological measures
        self.C = None
        self.A = None
        # T is the number of tips, as defined in O Dwyer
        self.T = None
        self.index = index

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
            #return 1 # constant waiting time
            #return np.random.exponential(1)  # constant Poisson
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
        if sigma == 0:
            dn_1 = 0
            dn_2 = 0
        else:
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

    def get_edge_length(self, clock):
        if self.left is None and self.right is None:
            # this is a tip
            return clock - self.born
        else:
            return self.spec - self.born

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
                       + ':' + str(self.spec-self.born)


class Tree:
    def __init__(self, n=1, r_e=0, R_0=0):
        '''
        R_0 adjusts the extrinction rate
        r_e adjusts the boundary
        n_0 sets the niche of the root node
        '''
        self.root = Node(n, r_e, R_0, born_time=0)
        self.node_list = []  # in simulte(), root will be added
        self.length = None

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
                if curr.spec == np.inf:
                    # print('All nodes stops speciating at size %d, please\
                    #        try again or adjust the parameters' % size)
                    return False, size
                clock = curr.spec  # forward time to spec time
                if not curr.alive:
                    continue
                # give birth to two nodes at clock time
                left, right = curr.speciation(mu, sigma, clock)
                if left.alive:
                    active_nodes.put(left)
                    left.index = size
                    size += 1
                if right.alive:
                    active_nodes.put(right)
                    right.index = size
                    size += 1
            else:
                # print('The system went extinct at size %d, please\
                #        try again or adjust the parameters' % size)
                return False, size
        self.length = clock
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

    def prune(self, node):
        if not node.visible:
            raise ValueError('Calling prune on invisible node')
        curr = node
        self.node_list.append(node)
        while True:
            if curr.left is None and curr.right is None:
                node.spec = curr.spec
                node.left = None
                node.right = None
                return

            if curr.left.visible and curr.right.visible:
                # reaching the speciation point
                node.spec = curr.spec
                node.left = curr.left
                node.right = curr.right
                self.prune(node.left)
                self.prune(node.right)
                return

            if curr.left.visible:
                curr = curr.left
                continue
            elif curr.right.visible:
                curr = curr.right
                continue

    def get_AC_list(self, threshold):
        return self._get_AC_list(self.root, threshold)

    def _get_AC_list(self, node, threshold):
        # Threshold is used to filter out earlier stage nodes
        if node.left is None and node.right is None:
            if node.index < threshold:
                return []
            return [[node.get_A(), node.get_C()]]
        left_lst = self._get_AC_list(node.left, threshold)
        right_lst = self._get_AC_list(node.right, threshold)
        result_lst = left_lst + right_lst
        if node.index > threshold:
            result_lst.append([node.get_A(), node.get_C()])
        return result_lst

    def get_EAD_list(self, clock, threshold):
        return self._get_EAD_list(self.root, clock, threshold)

    def _get_EAD_list(self, node, clock, threshold):
        if node.left is None and node.right is None:
            if node.index < threshold:
                return []
            return [[node.get_T(), node.get_edge_length(clock)]]
        left_lst = self._get_EAD_list(node.left, clock, threshold)
        right_lst = self._get_EAD_list(node.right, clock, threshold)
        result_lst = left_lst + right_lst
        if node.index > threshold:
            result_lst.append([node.get_T(), node.get_edge_length(clock)])
        return result_lst

    def get_misc(self):
        lst = []
        for node in self.node_list:
            i = node.index
            b = node.born
            t = node.get_T()
            a = node.get_A()
            n = node.n
            lst.append(np.array([i, b, t, a,  n]))
        return lst

    def prune_tree(self):
        self.prune(self.root)
        return

    def save_tree(self, clock, filename, pruned=True):
        tree_str = self.root.to_string(clock)
        f = open(filename, 'w')
        f.write(tree_str)
        f.close()
        return


def extinction(x):
    # x should be a Node object
    if x.get_e() > np.random.uniform():
        x.alive = False
    return
