class FibonacciHeap:

    class Node:
        def __init__(self, info):
            self.info = info
            self.left = self.right = self.child = self.parent = None
            self.degree = 0
            self.marked = False
    
    def __init__(self):
        self.root_list = self.min_node = None
        self.nrof_nodes = 0
        self.heap_arr = {-1: [None, False]}
    
    def add_to_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
            self.root_list.left = node
            self.root_list.right = node
        else:
            # Adds the new node after the first node in the root list.
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node
        if not self.min_node or node.info < self.min_node.info:
            self.min_node = node
        self.nrof_nodes += 1
        if node.info not in self.heap_arr:
            self.heap_arr[node.info] = [node, True]
        else: self.heap_arr[node.info][1] = True
    
    def remove_from_root_list(self, node):
        self.nrof_nodes -= 1
        self.heap_arr[node.info][1] = False
        if node == node.right:
            self.root_list = None
            return
        if node == self.root_list:
            self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left
    
    def add_to_child_list(self, parent, node):
        parent.degree += 1
        self.nrof_nodes += 1
        node.parent = parent
        if node.info not in self.heap_arr:
            self.heap_arr[node.info] = [node, True]
        else: self.heap_arr[node.info][1] = True
        if parent.child == None:
            parent.child = node
            parent.child.left = node
            parent.child.right = node
            return
        # Adds the new node after the first node in the child list.
        node.right = parent.child.right
        node.left = parent.child
        parent.child.right.left = node
        parent.child.right = node
    
    def remove_from_child_list(self, parent, node):
        parent.degree -= 1
        self.nrof_nodes -= 1
        self.heap_arr[node.info][1] = False
        if node == node.right:
            parent.child = None
            return
        if node == parent.child:
            parent.child = node.right
        node.left.right = node.right
        node.right.left = node.left

    def iterate_list(self, head):
        if head == None:
            return "Empty list."
        current = stop = head
        finished = False
        while True:
            if finished and current == stop:
                break
            elif current == stop:
                finished = True
            yield current
            current = current.right

    def find_min(self):
        return self.min_node

    def merge(self, heap):
        temp_heap = FibonacciHeap()
        temp_heap.root_list = self.root_list
        # linking last node from first heap with first node from second heap
        temp_heap.root_list.left.right = heap.root_list
        # linking last node from second heap with first node from first heap
        heap.root_list.left.right = temp_heap.root_list
        # linking first node from first heap with last node from second heap
        temp_heap.root_list.left = heap.root_list.left
        # linking first node from second heap with last node from first heap
        heap.root_list.left = self.root_list.left
        if self.min_node.info > heap.min_node.info:
            temp_heap.min_node = heap.min_node
        else:
            temp_heap.min_node = self.min_node
        temp_heap.nrof_nodes = self.nrof_nodes + heap.nrof_nodes
        return temp_heap

    def heap_link(self, y, x):
        '''Links y - bigger info node - to x - smaller info node - in root list according to min heap property.'''
        self.remove_from_root_list(y)
        self.add_to_child_list(x, y)
        y.parent = x
        y.mark = False

    def consolidate(self):
        '''
        Links trees of equal degrees respecting the min heap property.
        Stops when there are no trees of equal degrees in root list.
        '''
        tree_of_degree = [None] * self.nrof_nodes
        nodes = [x for x in self.iterate_list(self.root_list)]
        for w in range(0, len(nodes)):
            x = nodes[w]
            d = x.degree
            while tree_of_degree[d] != None:
                y = tree_of_degree[d]
                if x.info > y.info:
                    x, y = y, x
                self.heap_link(y, x)
                tree_of_degree[d] = None
                d += 1
            tree_of_degree[d] = x
        # Determining new min value by running through the roots of all newly created trees.
        for i in range(0, len(tree_of_degree)):
            if tree_of_degree[i] is not None:
                if not self.min_node:
                    self.min_node = tree_of_degree[i]
                if tree_of_degree[i].info < self.min_node.info:
                    self.min_node = tree_of_degree[i]

    def extract_min(self):
        '''Extracts min node from heap and makes all its children roots then consolidates heap.'''
        z = self.min_node
        if z is not None:
            if z.child is not None:
                children = [x for x in self.iterate_list(z.child)]
                for i in range(0, len(children)):
                    self.add_to_root_list(children[i])
                    children[i].parent = None
            self.remove_from_root_list(z)
            self.min_node = None
            self.consolidate()
        return z

    def cut(self, child, parent):
        self.remove_from_child_list(parent, child)
        self.add_to_root_list(child)
        child.parent = None
        child.mark = False

    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)
    
    def decrease_key(self, x, k):
        if k > x.info:
            return None
        x.info = k
        y = x.parent
        if y is not None and x.info < y.info:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.info < self.min_node.info:
            self.min_node = x
   
    def delete(self, val):
        self.decrease_key(self.heap_arr[val][0], -1)
        return self.extract_min()


input_file = open("input.txt", 'r')
output_file = open("output.txt", 'w')
n = int(input_file.readline())
my_heap = FibonacciHeap()
for _ in range(n):
    line = list(map(int, input_file.readline().split()))
    if line[0] == 1:
        node = FibonacciHeap.Node(line[1])
        my_heap.add_to_root_list(node)
    if line[0] == 2:
        my_heap.delete(line[1])
    if line[0] == 3:
        output_file.write(str(my_heap.find_min().info) + '\n')
    if line[0] == 4:
        my_heap.extract_min()
        



