import Graph_Sampling
import networkx as nx
import HeterogeneousNetwork as hn
import matplotlib.pyplot as plt
import os, sys, random, time

def output_sample(output_file, sampling):
	file = open(output_file,"w")
	for edges in sampling.edges():
		file.write(edges[0] + "\t" + edges[1] + "\t1\n")
	file.close()

dataset = sys.argv[1]
size = int(sys.argv[2])
output_dir = sys.argv[3]
method = sys.argv[4]

print(output_dir)
reached = {}
nt = hn.HeterogeneousNetwork()
nt.loadCSV(dataset)

lista = nt.getNodes()
random.shuffle(lista)
node_seed = lista[0]

sampled_subgraph = nx.Graph()

print(node_seed)
file_unreached = open(output_dir + "/unreached.txt","w")
count = 0
while len(reached) < len(nt.getNodes()):
	if method == 'SRW':
		object = sampling.SRW_RWF_ISRW()
		sampled_subgraph = object.random_walk_sampling_simple(nt.net,size,node_seed)
	elif method == 'RWF':
		arg = float(sys.argv[5])
		object = sampling.SRW_RWF_ISRW()
		sampled_subgraph = object.random_walk_sampling_with_fly_back(nt.net,size,arg,node_seed)
	elif method == 'ISRW':
		object = sampling.SRW_RWF_ISRW()
		sampled_subgraph = object.random_walk_induced_graph_sampling(nt.net,size,node_seed)
		sampled_subgraph = nt.net.subgraph(sampled_subgraph)
	elif method == 'SB':
		arg = int(sys.argv[5])
		object = sampling.Snowball()
		sampled_subgraph = object.snowball(nt.net,size,arg,node_seed)
	elif method == 'FF':
		object = sampling.ForestFire()
		sampled_subgraph = object.forestfire(nt.net,size,node_seed)
	elif method == 'MHRW':
		object = sampling.MHRW()
		sampled_subgraph = object.mhrw(nt.net,size,node_seed)
	elif method == 'Induced-MHRW':
		object = sampling.MHRW()
		sampled_subgraph = object.induced_mhrw(nt.net,size,node_seed)

	lista = list(sampled_subgraph.nodes())
	alcancou = False
	for node in lista:
		if node not in reached:
			reached[node] = True
			alcancou = True

	if alcancou:
		print("Nodes:", len(sampled_subgraph.nodes),' Edges:', len(sampled_subgraph.edges()))
		print("Nodes:", len(reached), '/', len(nt.getNodes()))
		print()
		count += 1
		output_sample(output_dir +'/' + str(count) + '.network', sampled_subgraph)
	else:
		print('unreached:', node_seed)
		reached[node_seed] = False
		file_unreached.write(node_seed + "\n")
	if node_seed:
		for node in nt.getNodes():
			if node not in reached:
				node_seed = node
				break
file_unreached.close()
