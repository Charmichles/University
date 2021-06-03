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


def secondBestMST(G : WeightedGraph, algoritmAPCM):
    fout = open("SecondBestMST.out", 'w')

    T = None
    if algoritmAPCM == 'Kruskal':
        T = G.KruskalMST()
    elif algoritmAPCM == 'Prim':
        T = G.PrimMST()
    else:
        raise Exception("Pentru secondBestMST parametrul algoritmAPCM trebuie sa fie egal cu 'Kruskal' sau 'Prim'\n")
    cost_mst = sum([muchie.cost for muchie in T])

    # fac o lista cu label-ul varfurilor din MST
    mst_node_labels = set()
    for edge in T:
        mst_node_labels.add(edge.vertex1)
        mst_node_labels.add(edge.vertex2)
    # creez un dictionar care asociaza label-ul unui nod cu obiectul nod propriu-zis din Tree
    mst_nodes = dict( [(label, TreeNode(TreeNodeInfo(sys.maxsize, label))) for label in mst_node_labels] )
    mst = Tree(mst_nodes)
    adj_set_mst = WeightedGraph.get_adjacency_set(T)

    # am vazut la problema Graf Dinamic cum putem determina daca exista un APCM cu cost mai mic prin inchiderea unui ciclu si eliminarea muchiei maxime
    # are sens atunci sa pot obtine si un APCM cu cost mai mare prin acelasi procedeu astfel:
    # - pentru fiecare muchie care nu este in APCM o sa o adaug la APCM, astfel inchizand un ciclu
    # - elimin muchia maxima din ciclul format(excluzand muchia tocmai adaugata) si calculez costul noului APCM in O(1)
    # - compar aceste rezultate intre ele, iar minimul este al doilea cel mai bun APCM
    adj_set_G = WeightedGraph.get_adjacency_set(G.edges)
    edges_notinMST = []
    aux_set = set()
    # fac lista cu muchii care nu sunt in APCM
    for vertex1, adj_vertex1 in adj_set_G.items():
        for vertex2, cost in adj_vertex1.items():
            if adj_set_mst.get(vertex1).get(vertex2) is None and (vertex1, vertex2) not in aux_set:
                edges_notinMST.append(WeightedGraphEdge(vertex1, vertex2, cost))
                aux_set.add((vertex1, vertex2))
                aux_set.add((vertex2, vertex1))

    edge_old, edge_new = None, None
    cost_secondbestMST = None
    for edge in edges_notinMST:
        # fac muchia maxima(exceptand muchia adaugata) din ciclul inchis de muchia adaugata
        mst_nodes = dict( [(label, TreeNode(TreeNodeInfo(sys.maxsize, label))) for label in mst_node_labels] )
        mst.nodes = mst_nodes
        mst.link_nodes(mst_nodes[edge.vertex1], adj_set_mst)

        cycle_labels = mst.find(mst_nodes[edge.vertex2])
        
        cycle_edges = []
        for i in range(len(cycle_labels) - 1):
            cycle_edges.append(WeightedGraphEdge(cycle_labels[i], cycle_labels[i+1], adj_set_G[cycle_labels[i]][cycle_labels[i+1]]))

        max_edge = max(cycle_edges, key = lambda edge : edge.cost)
        # calculez costul noului APCM si compar
        cost_new = cost_mst - max_edge.cost + edge.cost
        if cost_secondbestMST is None or cost_new < cost_secondbestMST:
            cost_secondbestMST = cost_new
            edge_old = max_edge
            edge_new = edge

    fout.write(f'Primul\nCost {cost_mst}\nMuchii\n')
    for edge in T:
        fout.write(f'{edge.vertex1} {edge.vertex2}\n')
    fout.write(f'Al doilea\nCost {cost_secondbestMST}\nMuchii\n')
    for edge in T:
        if ((edge.vertex1 == edge_old.vertex1 and edge.vertex2 == edge_old.vertex2) or
            (edge.vertex1 == edge_old.vertex2 and edge.vertex2 == edge_old.vertex1)):
            fout.write(f'{edge_new.vertex1} {edge_new.vertex2}\n')
        else:
            fout.write(f'{edge.vertex1} {edge.vertex2}\n')


if __name__ == '__main__':
    grafDinamic(WeightedGraph(file=open('grafpond.in', 'r')), WeightedGraphEdge(3, 5, 4), 'Prim')
    secondBestMST(WeightedGraph(file=open('secondBestMST.in', 'r')), 'Kruskal')