'''
	
'''
import os, sys, json

def readFile(model_path):
	keepFile = False
	f = open(model_path, "r")
	for line in f:
		if len(line.split('\t')) < 2:
			continue
		node, array = line.split('\t')
		if node not in merged_nodes:
			keepFile = True
			array = array.split('\n')[0].split(',')
			#print(node, array)
			if node in merging:
				merging[node]['count'] = merging[node]['count'] + 1
				for i in range(len(array)):
					merging[node]['F'][i] = merging[node]['F'][i] + float(array[i])
			elif len(merging) < max_lines:
				merging[node] = {'count': 1, 'F': [float(x) for x in array]}
	f.close()
	return keepFile

with open(sys.argv[1], "r") as read_file:
    params = json.load(read_file)

output_file = params['merge_output_file']

regularization_dir = params['regularization_output_dir']

sampled_models = []

merged_nodes = {}
max_lines = 0
for file in os.scandir(regularization_dir):
		if file.is_file():
			sampled_models.append(file.path)
			lines = sum(1 for line in open(file.path))
			if lines > max_lines:
				max_lines = lines
print(max_lines)
while len(sampled_models) > 0:
	print('==============================',len(sampled_models), ' | ', len(merged_nodes),'==============================')
	temp = []
	merging = {}
	while len(sampled_models) > 0:
		file = sampled_models.pop(0)
		if readFile(file):
			temp.append(file)
	sampled_models = temp
	f = open(output_file, "a")
	for node in merging:
		count = merging[node]['count']
		merged_nodes[node] = True
		f.write("\t".join([node, ",".join([str(x/count) for x in merging[node]['F']])]) + "\n")
	f.close();
