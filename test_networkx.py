import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_node('a', demand = -5)
G.add_node('a', demand = 0)
G.add_node('d', demand = 5)
G.add_edge('a', 'b', weight = 3, capacity = 4)
G.add_edge('a', 'c', weight = 6, capacity = 10)
G.add_edge('b', 'd', weight = 1, capacity = 9)
G.add_edge('c', 'd', weight = 2, capacity = 5)
G.add_edge(1, 2, weight = 3)

#flow_cost = nx.min_cost_flow_cost(G)
#print flow_cost

print G.node