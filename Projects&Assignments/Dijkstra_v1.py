import networkx as nx
import matplotlib.pyplot as plt

def Dijkstra(G, start, end):
    RG = G.reverse()
    dist = {}
    previous = {}
    for v in RG.nodes():
        dist[v] = float('inf')
        previous[v] = 'none'
    dist[end] = 0
    u = end
    while u != start:
        u = min(dist, key=dist.get)
        distu = dist[u]
        del dist[u]
        for u, v in RG.edges(u):
            if v in dist:
                alt = distu + RG[u][v]['weight']
                if alt < dist[v]:
                    dist[v] = alt
                    previous[v] = u
    path = (start,)
    last = start
    while last != end:
        nxt = previous[last]
        path += (nxt,)
        last = nxt
    return path


G = nx.DiGraph()
G.add_edge(0, 1, weight=80)
G.add_edge(1, 2, weight=50)
G.add_edge(1, 3, weight=30)
G.add_edge(3, 2, weight=10)
G.add_edge(2, 4, weight=20)
G.add_edge(2, 5, weight=30)
G.add_edge(4, 5, weight=10)
G.add_edge(5, 3, weight=5)
G.add_edge(2, 6, weight=10)
G.add_edge(4, 6, weight=10)
G.add_edge(3, 6, weight=25)
G.add_edge(5, 6, weight=35)

rs = Dijkstra(G, 0, 6)
nx.draw(G,with_labels=True)
print(rs)
plt.show()
