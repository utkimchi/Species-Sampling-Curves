import csv
import os
import pandas as pd
import numpy as np
import tempfile
import subprocess
import time



def runr(huc = "huc"):
	if "'" in huc:
		huc = huc.replace("'","\\'")
	print(huc)

	w_table = "write.table(asym, 'asym_" + huc + ".txt', sep=',');"

	theR = "suppressMessages(library(vegan));"
	theR += "setwd('D:/Colton_Data/Species_Accumulation/ssasymp_tables');" #Make sure you change to directory w/ computer you're working on
	theR += "sp1 <- read.csv('temp.csv');"
	theR += "sp1$X <- NULL;"
	theR += "sp2 <- specaccum(sp1, w=NULL);"
	theR += "mod1 <-fitspecaccum(sp2, 'asymp');"
	theR += "asym <- coef(mod1);"
	theR += w_table

	text_file = open('TemporaryR.txt' , 'w')
	text_file.write(theR)
	text_file.close
	subprocess.Popen("Rscript --vanilla D:/Colton_Data/Species_Accumulation/TemporaryR.txt")



#Empty Lists
sighting_dic = {} #Appends taxon onto collecting events
col_keys = [] #Collecting of collecting events
taxon = [] # Taxon
huc8s = [] #HUC8 Key, with collecting event taxon plis





#Creates dataframe with 0 - MRB / 1 - HUC8Name / 2 = Taxon / 3 = Collecting Id
df = pd.read_csv('Data/spaccu.csv', header=None , sep=',')

#Generates array of unique HUC 8 names
for row in df.itertuples():
	if row[2] not in huc8s:
		huc8s.append(row[2])

#Run the R for each individual HUC8
for huc in huc8s:
	#Clears previous list if filled
	taxon.clear()
	col_keys.clear()
	sighting_dic.clear()

	#Runs through each row in "spaccu.csv"
	for row in df.itertuples():
		if row[2] == huc: #checks if row is in in huc
			if row[3] not in taxon: #Adds unique taxon to list
				taxon.append(row[3])
			if row[4] not in col_keys: #adds unique collecting ids to list
				col_keys.append(row[4])
				sighting_dic.setdefault(row[4],[]) #set key for dict
			sighting_dic[row[4]].append(row[3]) #append tax

	specAccT = {}

	#For each unique species within HUC set value to 1 if it's the first time it has been seen
	#in the HUC, else set it to zero
	for x in taxon:
		specAccT.setdefault(x,[])
		for y in col_keys:
			if x in sighting_dic[y]:
				specAccT[x].append(1)
			else:
				specAccT[x].append(0)

	#Create dataframe
	dataFinal = pd.DataFrame(specAccT)
	count_row = dataFinal.shape[0]

	#
	if count_row > 1:
		dataFinal.to_csv('ssasymp_tables/temp.csv',sep=',')
		runr(huc)
	else:
		print(huc + "is not sampled enough")
	time.sleep(5)