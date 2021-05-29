import sys
from dataclasses import dataclass
from time import time
from functools import wraps
from FibonacciHeap import FibonacciHeap
from DisjointSet import DisjointSet, DisjointSetNode


# din proiectul meu pentru IA - o functie decorator pentru timpul de rulare a altei functii
# https://github.com/Charmichles/Facultate/blob/master/pygame-checkers/main.py
def timing(f):
    '''
        Decorator which prints the execution time of a function using the time package.\n
        The wraps decorator ensures that the decorated function does not take the definition of the wrap(*args, **kwargs) function.\n
        https://stackoverflow.com/questions/308999/what-does-functools-wraps-do
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        time_start = time()
        result = f(*args, **kwargs)
        time_end = time()
        print('\nUsing function {} took {} seconds.'.format(f.__name__, time_end - time_start))
        return result
    return wrap


@dataclass(order=True)
class WeightedGraphEdge:
    vertex1 : int
    vertex2 : int
    cost : int


class WeightedGraph:

    def __init__(self, vertex_no = 0, edge_no = 0, edges = None, file = None):
        self.vertex_no = vertex_no
        self.edge_no = edge_no
        self.edges = edges
        if file is not None:
            self.read_from_file(file)
    
    def add_edge(self, edge):
        self.edges.append(edge)
    
    def read_from_file(self, file):
        self.vertex_no, self.edge_no = tuple(map(int, file.readline().split()))
        self.edges = []
        while line := file.readline():
            vertex1, vertex2, cost = tuple(map(int, line.split()))
            self.edges.append(WeightedGraphEdge(vertex1, vertex2, cost))
    
    def __str__(self):
        return '\n'.join(map(str, self.edges))
    
    def get_adjacency_set(edges, directed = False):
        adj_set = dict()
        for edge in edges:
            if edge.vertex1 not in adj_set:
                adj_set[edge.vertex1] = dict()
            if not directed and edge.vertex2 not in adj_set:
                adj_set[edge.vertex2] = dict()
            adj_set[edge.vertex1][edge.vertex2] = edge.cost
            if not directed:
                adj_set[edge.vertex2][edge.vertex1] = edge.cost
        return adj_set

    @timing
    def get_BFS(edges, start_idx):
        adj_set = WeightedGraph.get_adjacency_set(edges)
        bfs = [start_idx]
        visited = set()
        visited.add(start_idx)
        left = 0
        while left < len(bfs):
            curr = bfs[left]
            for adj_vertex in adj_set[curr]:
                if adj_vertex not in visited:
                    visited.add(adj_vertex)
                    bfs.append(adj_vertex)
            left += 1
        return bfs

    @timing
    def KruskalMST(self):
        self.edges = sorted(self.edges, key = lambda edge : edge.cost)
        sorted_iter = iter(self.edges)
        nodes = dict( [ (idx, DisjointSetNode(idx)) for idx in range(1, self.vertex_no + 1) ] )
        # creez un DisjointSet in care sunt initial un nr. de subset-uri egale cu nr. de varfuri din graf, iar fiecare nod e propriul parinte
        disjointSet = DisjointSet(nodes.values())
        mst_edges = []
        while len(mst_edges) < self.vertex_no - 1:
            edge = next(sorted_iter)
            x = disjointSet.find(nodes[edge.vertex1])
            y = disjointSet.find(nodes[edge.vertex2])
            # daca prin adaugarea muchiei nu se creeaza un ciclu, adica daca in DisjointSet varfurile muchiei nu fac parte din acelasi subset
            if x != y:
                mst_edges.append(edge)
                disjointSet.union(x, y)
        return mst_edges
    
    @timing
    def PrimMST(self):

        # clasa pe care o folosesc pentru informatia din nodurile inserate in heap
        # am nevoie cost si de numarul varfului
        @dataclass(order=True, frozen=True)
        class NodeInfo:
            cost : int
            index : int
        
        
        parents = [0] * (self.vertex_no + 1)
        minHeap = FibonacciHeap(self.vertex_no)
        nodes = dict( [ (idx, FibonacciHeap.Node(NodeInfo(sys.maxsize, idx))) for idx in range(1, self.vertex_no + 1) ] )
        # initial, toate varfurile au costul +INF in heap
        for node in nodes.values():
            minHeap.add_to_root_list(node)
        # pentru varful de plecare costul este 0, ca sa fie luat primul din heap
        minHeap.decrease_key(nodes[1], NodeInfo(0, 1))

        adj_set = WeightedGraph.get_adjacency_set(self.edges)
        while not minHeap.isEmpty():
            # extrag varful cu costul minim
            minNode = minHeap.extract_min()
            # parcurg varfurile adiacente celui extras
            for new_idx, new_cost in adj_set[minNode.info.index].items():
                # daca un varf adiacent nu a fost adaugat inca la APCM si distanta pana la el prin varful extras e mai mica decat distanta calculata anterior
                if minHeap.inHeap(nodes[new_idx].info) and new_cost < nodes[new_idx].info.cost:
                    # parintele in APCM al varfului adiacent este varful extras
                    parents[new_idx] = minNode.info.index
                    # actualizez costul in heap
                    minHeap.decrease_key(nodes[new_idx], NodeInfo(new_cost, new_idx))
        
        return [WeightedGraphEdge(i, parents[i], adj_set[i][parents[i]]) for i in range(2, len(parents))]

