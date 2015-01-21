#!/bin/bash
mkdir out
for fname in $( ls "playground/" ); do
	f="playground/$fname"
	echo "performing $f"	
	mv $f domains
	python query.py
	output="out/data_$fname"
	touch "$output"
	echo outputting to "$output"
	for result in $( ls "data" ); do
		echo processing "data/$result"
		cat "data/$result" >> "$output"
		rm "data/$result"
	done
	gzip $output
	echo finished "$fname"
done
echo finished all
