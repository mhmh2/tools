#!/bin/bash

if [ $# -gt 2 ]; then
	echo "you entered more than one paramter."
	echo "usage: ./script <domain name>"
	echo "Example: ./script hackerone.com"
	exit 1
fi

if [ ! -d "thirdlevels" ]; then
	mkdir thirdlevels
fi


if [ ! -d "scans" ]; then
	mkdir scans
fi


if [ ! -d "eyewitness" ]; then
	mkdir eyewitness
fi


pwd=$(pwd)

echo "subdomain enumartion with sublist3r... "
sublist3r -d $1 -o final.txt

echo $1 >> final.txt

echo "compiling third-level domains..."
cat domains-test.txt | grep -Po "(\w+\.\w+\.\w+)$" | sort -u >> third-level.text


echo "Gathering all sudomains from the third-level... "
for domian in $(cat third level.txt) do sublist3r -d $domian -o /thirdlevel/$domain.txt; cat thirdlevel/$domain.txt | sort -u >> final.txt ; done


if [ $# -eq 2 ]; then
	echo "Checking if the third-level doamains are alive or not..."
	cat final.txt | sort -u | grep -v $2 | httprobe -s -p 443 | sed 's/https\?:\/\///' | tr -d ":443" > alive_verfied.txt
else
	echo "Checking if the third-level domains are alive or not..."
	cat final.txt | sort -u | httprobe -s -p 443 | sed 's/https\?:\/\///' | tr -d ":443" > alive_verfied.txt
fi


echo "Scaning alive hosts with namp..."
nmap -iL alive_verfied.txt -T5 -oA /scans/scanned.txt


echo "Running eye witness..."
eyewitness -f $pwd/alive_verfied.txt $1 --all-protcols
mv /usr/share/eyewitness/$1 /eyewitness/$1





