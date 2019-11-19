import csv
import pandas as pd
import numpy as np
import glob as gb 

huc_asym ={}

#Grabs filenames
fList = gb.glob("asym_tables/*.txt")

print(fList)

for li in fList:
	#Extracts HUC8s
	fSplit = li.split('_')
	sSplit = fSplit[2].split('.')
	huc8 = sSplit[0]

	#Sets up dict with huc8:asymptote 
	lineCount = 0
	with open (li, "r") as f:
		for line in f:
			lineCount+=1
			if lineCount == 2:
				spLine = line.split(',')
				tempString = spLine[1]
				asym_value = tempString[0:5]
				huc_asym[huc8] = asym_value


pp = pd.DataFrame.from_dict(huc_asym, orient='index', columns=['asym'])


pp.to_csv('lo_huc8_asym.csv')