import numpy as np
import networkx as nx
import pandas as pd
import gurobipy as gb
from gurobipy import GRB

# load data fram using pandas for topology
df = pd.read_csv("data/ATT/topology.txt", delimiter=r"\s+")
print(df)

# Create Graph

G = nx.from_pandas_edgelist(df, 'from_node', 'to_node', ['capacity', 'prob_failure'])

#Draw loaded graph
# spring layout prevents graph from
# becoming too clustered
layout = nx.spring_layout(G)
# draw node, edges, and labels sperately
nx.draw_networkx_labels(G, pos=layout )
nx.draw_networkx_nodes(G, pos=layout) 
nx.draw_networkx_edges(G, pos=layout)
# only add capacities as labels
edge_labels = dict([((source, dest), G[source][dest]["capacity"]) for source, dest in G.edges])
print(edge_labels)
nx.draw_networkx_edge_labels(G, pos= layout, edge_labels= edge_labels,font_color="red", font_weight="bold", font_size = 5)


demands = np.loadtxt("data/ATT/demand.txt")
## get the maximum value for each column
## reshape demands matrix
demands_matrix = np.amax(demands, axis = 0).reshape(25,25)
print(demands_matrix.shape)


m = gb.Model("step4")
traffic = {}
for (i, j) in demands_dict:
    if (i, j) in edge_labels:
        traffic[(i, j)] = m.addVar(ub=edge_labels[(i, j)], name=f"traffic_{i}_{j}")
    else:
        traffic[(i, j)] = m.addVar(ub=0, name=f"traffic_{i}_{j}")
        
for (i, j) in demands_dict:
    print((i, j))
    m.addConstr(gb.quicksum((traffic[(i, j)] - traffic[(j, i)]) for (i, j) in demands_dict) == demands_dict[(i , j)])
for (i, j) in edge_labels:
    m.addConstr(gb.quicksum((traffic[(i, j)]) for (i,j) in demands_dict) <= edge_labels[(i, j)])

m.setObjective(gb.quicksum(traffic[(i, j)] for (i, j) in demands_dict), GRB.MAXIMIZE)

m.optimize()

if m.status == GRB.OPTIMAL:
    print('Optimal traffic allocation')