from __future__ import annotations
from dataclasses import dataclass


@dataclass(init=False, eq=False)
class DisjointSetNode:
    parent : DisjointSetNode
    info : int
    rank : int

    def __init__(self, info):
        self.parent = self
        self.info = info
        self.rank = 0
    
    def __eq__(self, node):
        return self.info == node.info


# https://en.wikipedia.org/wiki/Disjoint-set_data_structure#Making_new_sets
# https://stackoverflow.com/a/18083181 - unde am citit mai multe despre cum functioneaza rank-ul
class DisjointSet:

    def __init__(self, nodes):
        self.nodes = nodes

    def add(self, node):
        self.nodes.append(node)
    
    # path compression with recursion
    def find(self, node):
        if node.parent != node:
            # fac parintele fiecarui nod de pe drumul dintre nodul dat si root sa fie root-ul
            # reduce numarul de noduri care trebuie traversate atunci cand se reapeleaza functia cu acelasi nod sau cu fii lui
            node.parent = self.find(node.parent)
            return node.parent
        else:
            return node
    
    # union by rank
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        # fac parte din acelasi subset, deci nu trebuie facut union
        if x == y:
            return
        
        # vreau sa-l fac pe x parinte, deci ar trebui sa fie nodul cu rank-ul mai mare
        if x.rank < y.rank:
            x, y = y, x
        
        # il fac pe x parinte si cresc rank-ul daca subset-urile aveau rank egal
        y.parent = x
        if x.rank == y.rank:
            x.rank += 1
