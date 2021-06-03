from dataclasses import dataclass


@dataclass
class NetworkEdge:
    vertex1 : int
    vertex2 : int
    capacity: int
    flux : int


class Network:

    def __init__(self, source = 0, sink = 0, vertex_no = 0, edge_no = 0, edges = None, file = None):
        self.source = source
        self.sink = sink
        self.vertex_no = vertex_no
        self.edge_no = edge_no
        self.edges = edges
        if file is not None:
            self.read_from_file(file)
    
    def read_from_file(self, file):
        self.vertex_no = int(file.readline())
        self.source, self.sink = tuple(map(int, file.readline().split()))
        self.edge_no = int(file.readline())
        self.edges = []
        while line := file.readline():
            vertex1, vertex2, capacity, flux = tuple(map(int, line.split()))
            self.edges.append(NetworkEdge(vertex1, vertex2, capacity, flux))
    
    def flux_is_correct(self):
        # node_flux = {node : [outbound_flux, inbound_flux]}
        node_flux = dict()
        for edge in self.edges:
            if edge.flux > edge.capacity:
                return False
            if edge.vertex1 not in node_flux:
                node_flux[edge.vertex1] = [0, 0]
            if edge.vertex2 not in node_flux:
                node_flux[edge.vertex2] = [0, 0]
            node_flux[edge.vertex1][0] += edge.flux
            node_flux[edge.vertex2][1] += edge.flux
        
        for node, flux in node_flux.items():
            if node != self.source and node != self.sink and flux[0] != flux[1]:
                return False
        return True
    
    def Edmonds_Karp(self):
        pass


if __name__ == '__main__':
    fout = open('retea.out', 'w')
    network = Network(file=open('retea.in', 'r'))
    fout.write("DA" if network.flux_is_correct() else "NU")
    fout.close()