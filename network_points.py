import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
points = [(1, 10), (8, 10), (10, 8), (7, 4), (3, 1)]  # (x,y) points
edges = [(0, 1, 10), (1, 2, 5), (2, 3, 25), (0, 3, 3), (3, 4, 8)]  # (v1,v2, weight)

for i in range(len(edges)):
    G.add_edge(points[edges[i][0]], points[edges[i][1]], weight=edges[i][2])

# you want your own layout
# pos = nx.spring_layout(G)
pos = {point: point for point in points}

# add axis
fig, ax = plt.subplots()
nx.draw(G, pos=pos, node_color='k', ax=ax)
nx.draw(G, pos=pos, node_size=1500, ax=ax)  # draw nodes and edges
nx.draw_networkx_labels(G, pos=pos)  # draw node labels/names
# draw edge weights
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
plt.axis("on")
ax.set_xlim(0, 11)
ax.set_ylim(0,11)
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
plt.show()