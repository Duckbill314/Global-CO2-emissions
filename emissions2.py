from pyvis.network import Network
import networkx as nx
import pandas as pd

# cleaning the data

data_set = set()

with open('Network_Data.csv', 'r', encoding='utf-8-sig') as network_data:
  lines = network_data.readlines()
  headers = lines[0].strip().split(",")
  for line in lines[1:]:
    strings = line.strip().split(",")
    row = (strings[0], strings[1], strings[2])
    reverse_row = (strings[1], strings[0], strings[2])
    if (row not in data_set) and (reverse_row not in data_set) and (row != reverse_row):
      data_set.add(row)

# populating series with cleaned data

dep_list = []
arr_list = []
emis_list = []

for (dep, arr, emis) in data_set:
  dep_list.append(dep)
  arr_list.append(arr)
  emis_list.append(float(emis))

# creating dataframe

data = {headers[0]: dep_list, headers[1]: arr_list, headers[2]: emis_list}
df = pd.DataFrame(data)

# generating graph and nodes

g = nx.Graph()

labels = df["DepCity"].tolist()
for i in range(len(labels)):
  g.add_node(labels[i], id=i)
  
# generating edges from dataframe

for i in range(len(df.index)):
  row = df.iloc[i][:]
  g.add_edge(row["DepCity"], row["ArrCity"], weight=row["CarbonEmissioninKg"])

# populating title fields with neighbour data for each node

for node, neighbours in g.adj.items():
  g.nodes[node]['title'] = 'Emissions [kg]'
  g.nodes[node]['size'] = len(neighbours)
  for neighbour, edge_attributes in neighbours.items():
    weight = edge_attributes['weight']
    g.nodes[node]['title'] += '<br>{}: {}'.format(neighbour, weight)
    
# creating the network

nt = Network('500px', '500px')
nt.from_nx(g)

# showing the network

nt.show('emissions.html')