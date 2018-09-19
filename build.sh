#!/bin/bash

for F in src/challenge*.py
do
	pyinstaller --onefile $F
done
