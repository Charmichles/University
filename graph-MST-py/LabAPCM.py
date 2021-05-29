from __future__ import annotations

# Lab APCM - https://drive.google.com/drive/u/0/folders/1gx37SoaLjPB-PLQ-SXGfK40e6QmWTAiQ
# Brihac Andrei, Grupa 233
# pentru restanta la laboratorul de Algoritmi Fundamentali

import sys
from Tree import Tree, TreeNode, TreeNodeInfo
from WeightedGraph import WeightedGraph, WeightedGraphEdge


def grafDinamic(G : WeightedGraph, e : WeightedGraphEdge, algoritmAPCM):
    fout = open('GrafDinamic.out', 'w')
    fout.write(f'Muchiile APCM in G folosind {algoritmAPCM}:\n')

    T = None
    if algoritmAPCM == 'Kruskal':
        T = G.KruskalMST()
    elif algoritmAPCM == 'Prim':
        T = G.PrimMST()
    else:
        raise Exception("Pentru grafDinamic parametrul algoritmAPCM trebuie sa fie egal cu 'Kruskal' sau 'Prim'\n")
    
    for edge in T:
        fout.write(f'{edge.vertex1} {edge.vertex2}\n')
    cost_apcm = sum([muchie.cost for muchie in T])
    fout.write(f'Cost total {cost_apcm}\n')

    # fac o lista cu label-ul varfurilor din MST
    mst_node_labels = set()
    for edge in T:
        mst_node_labels.add(edge.vertex1)
        mst_node_labels.add(edge.vertex2)
    # creez un dictionar care asociaza label-ul unui nod cu obiectul nod propriu-zis din Tree
    mst_nodes = dict( [(label, TreeNode(TreeNodeInfo(sys.maxsize, label))) for label in mst_node_labels] )
    mst = Tree(mst_nodes)
    # formeaza MST-ul propriu zis folosind unul dinte varfurile muchiei date ca radacina
    adj_set = WeightedGraph.get_adjacency_set(T)
    mst.link_nodes(mst_nodes[e.vertex1], adj_set)

    # ca sa gasesc ciclul este de ajuns sa urc din celalalt varf al muchiei date pana in radacina - O(n)
    cycle_labels = mst.find(mst_nodes[e.vertex2])
    
    cycle_edges = []
    for i in range(len(cycle_labels) - 1):
        cycle_edges.append(WeightedGraphEdge(cycle_labels[i], cycle_labels[i+1], adj_set[cycle_labels[i]][cycle_labels[i+1]]))
    cycle_edges.append(e)

    max_edge = max(cycle_edges, key = lambda edge : edge.cost)
    fout.write(f'Muchia de cost maxim din ciclul inchis de {e.vertex1} {e.vertex2} in APCM este {max_edge.vertex1} {max_edge.vertex2} de cost {max_edge.cost}\n')

    # am aflat muchia de cost maxim din ciclul inchis in APCM de muchia data
    # putem determina in O(1) daca prin adaugarea muchiei date noul graf creat are un APCM cu cost mai mic astfel:
    # daca costul muchiei date este mai mic decat costul maxim calculat mai devreme atunci putem inlocui acea muchie cu muchia data
    # costul noului APCM este costul vechi - costul muchiei maxime + costul muchiei date
    cost_apcm_nou = cost_apcm - max_edge.cost + e.cost if e.cost < max_edge.cost else cost_apcm
    fout.write(f'Dupa adaugarea muchiei APCM are costul {cost_apcm_nou}\n')

    fout.close()


if __name__ == '__main__':
    grafDinamic(WeightedGraph(file=open('grafpond.in', 'r')), WeightedGraphEdge(3, 5, 4), 'Prim')