from __future__ import annotations
from dataclasses import dataclass


@dataclass(order=True)
class TreeNodeInfo:
    cost : int
    label : int


@dataclass(init=False, eq=False)
class TreeNode:
    parent : TreeNode
    info : TreeNodeInfo
    depth : int

    def __init__(self, info):
        self.parent = None
        self.info = info
        self.depth = 0
    
    def __eq__(self, node):
        return self.info == node.info


class Tree:

    def __init__(self, nodes):
        self.nodes = nodes
    
    def add(self, node):
        self.nodes.add(node)
    
    def link_nodes(self, root, adj_set):
        queue = [root]
        visited = set()
        visited.add(root.info.label)
        left = 0
        while left < len(queue):
            curr = queue[left]
            for adj_vertex_label in adj_set[curr.info.label]:
                if adj_vertex_label not in visited:
                    adj_vertex = self.nodes[adj_vertex_label]
                    queue.append(adj_vertex)
                    visited.add(adj_vertex.info.label)
                    adj_vertex.info.cost = adj_set[curr.info.label][adj_vertex.info.label]
                    adj_vertex.parent = curr
                    adj_vertex.depth = curr.depth + 1
            left += 1

    def find(self, node):
        path = []
        while node.parent is not None:
            path.append(node.info.label)
            node = node.parent
        path.append(node.info.label)
        return path
