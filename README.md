# Transductive Classification for Sampled Networks - TCSN



## Dependences
This framework requires Java, python 3.5 or higher, libraries networkx and numpy.

```bash
pip install networkx numpy
```
## Usage
This repository comes pre-configured to download datasets and perform the sampling, regularization and merge of regularized samples.

```bash
./run
```

## Manual Configuration
### 1. Dataset
To run is required a dataset file where each line represents an edge in the following format:
```tsv
node1:layer1\tnode2:layer1\tweight
node2:layer1\tnode3:layer2\tweight
node3:layer2\tnode1:layer1\tweight
```
### 2. Labeled objects
Labeled file where each line represents a node and its respective label in onehot format, the file format is the following:
```tsv
node1:layer1\tclass1,class2,class3
node2:layer1\tclass1,class2,class3
```

### 3. Configuration file
You will need to edit the **params.json** file
```json
{
  "dataset": "/path/to/your/dataset",
  "labels": "/path/to/your/labels_file",
  "sampling_method": "sampling_method_to_use",
  "sampling_output_dir": "/path/to/your/sampling/output_dir",

  "mi": "0.1",
  "weight_relations": {
  	"layer1_layer1": "0.5",
  	"layer1_layer2": "0.5"
  },  
  "regularization_output_dir": "/path/to/your/regularizated_models/output_dir",

  "merge_output_file": "merged_model_output_name"
}
```
being that the parameters of GNetMine are:
- **mi:** Importance of labeled data during the propagation of labels, ranging from 0.1 to 1
- **weight_relations:** Weight of the relations between the layers, the name of the layers must be connected by 'underline' and the values will be automatically normalized when running GNetMine, all existing layer relations must be defined. If no pair of layers is specified all pairs of layers will have equal weights.

### 4. run
All commands are being run from the root folder of this repository

**4.1 Sampling**

If it is the first time running sampling script it is necessary to install the **Graph_Sampling** library to do this execute:
```bash
pip3.5 install --user -e Sampling/Graph_Sampling/
```

Run with sample size set using Chernoff Bounds
```bash
python3.5 Sampling/SamplingDataset.py json_file
```

Run with manually defined sample size. Commonly used if the sample size defined by Chernoff Bounds is larger than the system can regularize or if you wants to generate fewer samplings and consume more RAM by defining a larger sample size than defined by Chernoff Bounds.
```bash
python3.5 Sampling/SamplingDataset.py json_file sample_size
```

**4.2 Regularization**

After making the sampling of the dataset it is necessary to execute the regularization in each sampling for this to execute:
```bash
java -Xmx5G -cp Regularization/Transductive_Classifier.jar algoritmos.GNetMineSampling params.json
```

- **-Xmx5G** This parameter indicates that the java virtual machine will use up to 5GB of RAM, this value can be changed if it receives **java.lang.OutOfMemoryError** exception.

**4.3 Merge**

It aims to join the regularized samplings by averaging the array F of nodes that were regularized in different samplings, for this execute:

```bash
python3.6 Sampling/Merge.py params.json
```
