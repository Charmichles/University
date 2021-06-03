# Lab Drumuri Minime - https://drive.google.com/drive/u/0/folders/1gx37SoaLjPB-PLQ-SXGfK40e6QmWTAiQ
# Brihac Andrei, Grupa 233
# pentru restanta la laboratorul de Algoritmi Fundamentali

from WeightedGraph import WeightedGraph

def DijkstraSimplu(G : WeightedGraph, s, k):
    fout = open('DijkstraSimplu.out', 'w')
    drumuri = G.Dijkstra(s, k)
    cost_drumuri = [(drum, sum([muchie.cost for muchie in drum])) for drum in drumuri]
    drum_min = min(cost_drumuri, key = lambda pereche : pereche[1])
    fout.write(f'Cel mai apropiat punct de control este: {drum_min[0][0].vertex1}\n')
    fout.write(f'Costul drumului minim este: {drum_min[1]}\n')
    for muchie in drum_min[0]:
        fout.write(f'{muchie.vertex1} {muchie.vertex2}\n')
    fout.write('\n')

def DrumDeSigurantaMaxima(G : WeightedGraph, s, t):
    fout = open('dijkstra_retea.out', 'w')
    drumuri = G.Dijkstra(s, [t], directed=True)
    cost_drumuri = [(drum, sum([muchie.cost for muchie in drum])) for drum in drumuri]
    drum_min = min(cost_drumuri, key = lambda pereche : pereche[1])
    fout.write('Drumul de siguranta maxima este:\n')
    for muchie in reversed(drum_min[0]):
        fout.write(f'{muchie.vertex2} {muchie.vertex1}\n')
    fout.write('\n')

if __name__ == '__main__':
    DijkstraSimplu(WeightedGraph(file=open('grafdijkstra.in', 'r')), 1, [10, 6, 8])
    DrumDeSigurantaMaxima(WeightedGraph(file=open('dijkstra_retea.in', 'r')), 1, 7)