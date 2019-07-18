#!/bin/bash

# Usage: ./edge-sampling.sh input.network #number_of_edges #number_of_trials #output_dir

for i in $(seq $3)
do
	shuf $1 > $1.temp.shuf.$i
	split -l $2 $1.temp.shuf.$i ./$4/$i.network_
	rm $1.temp.shuf.$i
done
