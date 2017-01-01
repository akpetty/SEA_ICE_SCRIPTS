#!/bin/bash

for ((m=1980;m<=1999;m++)); do
    echo $m
	
	mv ./SIC/*$m* /Volumes/PETTY_PASSPORT2/ICE_CONC/BOOTSTRAP/ARCTIC/DAILY/$m/

done