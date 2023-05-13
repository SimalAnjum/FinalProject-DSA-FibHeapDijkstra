import math


class Heap:

    class Node:
        def __init__(self, key, value):
            self.key = key  # keyword
            self.value = value  # value of the node
            self.degree = 0  # elements of the heap
            self.p = None  # pointing to the parent node
            self.child = None  # points to the first child node
            self.left = None  # leftward loop pointer
            self.right = None  # rightward loop pointer
            self.mark = False  # flag

    total_nodes = 0
    roots, min = None, None

    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    def Insert(self, key, value=None):  # put on the left of min
        n = self.Node(key, value)
        n.left = n
        n.right = n

        if self.roots is None:
            self.roots = n
        else:
            n.right = self.roots.right
            n.left = self.roots
            self.roots.right.left = n
            self.roots.right = n

        if self.min is None or n.key < self.min.key:
            self.min = n

        self.total_nodes += 1

        return n

    def Minimum(self):
        return self.min

    def Union(self, heap):
        H = Heap()
        H.roots = self.roots
        H.min = self.min

        last = heap.roots.left
        heap.roots.left = H.roots.left
        H.roots.left.right = heap.roots
        H.roots.left = last
        H.roots.left.right = H.roots

        H.total_nodes = self.total_nodes + heap.total_nodes

        if heap.min.key < H.min.key:
            H.min = heap.min

        return H

    def ExtractMin(self):
        z = self.min
        if z is not None:
            if z.child is not None:
                children = [x for x in self.iterate(z.child)]
                for i in range(0, len(children)):
                    if self.roots is None:
                        self.roots = children[i]
                    else:
                        children[i].right = self.roots.right
                        children[i].left = self.roots
                        self.roots.right.left = children[i]
                        self.roots.right = children[i]
                    children[i].p = None

            if z == self.roots:
                self.roots = z.right
            z.left.right = z.right
            z.right.left = z.left

            if z == z.right:
                self.min = self.roots = None
            else:
                self.min = z.right
                self.Consolidate()
            self.total_nodes -= 1
        return z

    def Consolidate(self):
        A = [None] * self.total_nodes
        nodes = []
        for i in self.iterate(self.roots):
            nodes.append(i)

        for i in range(0, len(nodes)):
            x = nodes[i]
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    temp = x
                    x, y = y, temp
                self.Link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        for i in range(0, len(A)):
            if A[i] is not None:
                if A[i].key < self.min.key:
                    self.min = A[i]

    def Link(self, y, x):
        
        # remove the node root list
        
        if y == self.roots:
            self.roots = y.right
        y.left.right = y.right
        y.right.left = y.left

        y.left = y
        y.right = y

        # merge the node with child list of a root node

        if x.child is None:
            x.child = y
        else:
            y.right = x.child.right
            y.left = x.child
            x.child.right.left = y
            x.child.right = y

        x.degree += 1
        y.p = x
        y.mark = False

    def DecreaseKey(self, x, k):
        if k > x.key:
            return None
        x.key = k
        y = x.p
        if y is not None and x.key < y.key:
            self.Cut(x, y)
            self.CasCut(y)
        if x.key < self.min.key:
            self.min = x

    def Cut(self, x, y):

        # remove a node from child list

        if y.child == y.child.right:
            y.child = None
        elif y.child == x:
            y.child = x.right
            x.right.p = y
        x.left.right = x.right
        x.right.left = x.left

        y.degree -= 1

        # merge a node with root list

        if self.roots is None:
            self.roots = x
        else:
            x.right = self.roots.right
            x.left = self.roots
            self.roots.right.left = x
            self.roots.right = x

        x.p = None
        x.mark = False

    def CasCut(self, x):
        y = x.p
        if y is not None:
            if x.mark is False:
                x.mark = True
            else:
                self.Cut(x, y)
                self.CasCut(y)
