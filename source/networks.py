import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

print('\n\tThe Dataframe:\n\t(printing only 5 rows)\n')
data = pd.read_csv('datas.csv')
print(data.head()) # to see first rows of the dataframe (will return 5 rows by default)
print(data.columns) # to see all column titles of the dataframe
G = nx.from_pandas_edgelist(data, source='a_node_id',target='b_node_id',edge_attr=True, create_using=nx.DiGraph)

# Plot the graph
plt.figure(figsize=(20, 20))
nx.draw_networkx(G, with_labels=True)
plt.show()

# Metrics
# Yet to be added


#degree = in_degree + out_degree
print('Degree of 1416166971',G.degree(1416166971))

# Path with weight
print("\nThe shortest path with weights:\n", nx.shortest_path(G, source=2290884752, target=276846064, weight="distance"))
print("The length of the shortest path: ", nx.dijkstra_path_length(G, source=2290884752, target=276846064, weight="distance"))