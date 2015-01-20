#!/bin/bash
rm -rf data*
python query.py
touch data.tsv
cat header.txt >> data.tsv
dir="data/"
for fname in $( ls $dir ); do
	cat $dir$fname >> data.tsv
	rm $dir$fname
	echo finished $dir$fname
done
echo finished concatenating
gzip data.tsv
echo finished zipping
