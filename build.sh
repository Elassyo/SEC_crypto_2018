#!/bin/bash

for ID in 01 02 03 04 05 06 07 08 09 10 11 12 13 14
do
	if [ -e "src/challenge$ID.py" -a "src/challenge$ID.py" -nt "dist/challenge$ID" ]
	then
		pyinstaller --onefile "src/challenge$ID.py"
	fi
done
