import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

data = pd.read_csv('datas.csv')

G = nx.from_pandas_edgelist(data, source='a_node_id', target='b_node_id', edge_attr=True, create_using=nx.DiGraph)

plt.figure(figsize=(20,20))
nx.draw_networkx(G, with_labels=True)
plt.show()