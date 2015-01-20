#!/bin/bash
for fname in $( ls $dir ); do
	if [[ "$fname" == *.tsv ]]; then
		touch "$fname"2
		cat header $fname > "$fname"2
		mv "$fname"2 "$fname"
	fi
done
