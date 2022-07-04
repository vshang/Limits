#!/bin/sh
#Script to add fake observed limit to output of running combine fully blinded so limit_Victor.py can be run without changes

name=$1
echo "Adding fake observed limit of 0.0 to combine output for $name..."

for output in ${name}/*.txt
do
    if [ $(wc -l < $output) -le 5 ]; then
	sed -i '1i \0.0' $output
    fi
done

echo "Done adding fake observed limits to files in $name."
