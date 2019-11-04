import networkx as nx
import matplotlib.pyplot as plt
g = nx.DiGraph()
g.clear()
g.add_node("Dufu")
g.add_node("LiBai")
g.add_node("MengHaoran")
g.add_node("WangWei")
g.add_node("ZhangJiuling")
g.add_edges_from([("Dufu","LiBai"),])
g.add_edge("A","C")
g.add_edge("B","C")
g.add_edge("C","A")

nx.draw(g,with_labels=True)
plt.show()