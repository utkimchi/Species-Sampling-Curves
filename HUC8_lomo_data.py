import csv
import os
import pandas as pd
import numpy as np
import tempfile
import subprocess
import time

#PRINTS OUT GRAPHS



def runr(huc = "huc"):
	if "'" in huc:
		huc = huc.replace("'","\\'")
	elif "." in huc:
		huc = huc.replace(".","\\.")
	print(huc)
	w_table = "write.table(asym, 'asym_" + huc + ".txt', sep=',');"

	theR = "suppressMessages(library(vegan));"
	theR += "setwd('D:/Colton_Data/Species_Accumulation/asym_tables');" #Make sure you change to directory w/ computer you're working on
	theR += "sp1 <- read.csv('temp.csv');"
	theR += "sp1$X <- NULL;"
	theR += "sp2 <- specaccum(sp1, w=NULL);"
	theR += "mod1 <-fitspecaccum(sp2, 'lomolino');"
	theR += "mod2 <-fitspecaccum(sp2, 'asymp');"
	theR += "asym <- coef(mod1);"
	theR += w_table
	theR += "setwd('D:/Colton_Data/Species_Accumulation/test_graphs');"
	theR += "jpeg('sac_"+ huc + ".jpg');"
	theR += "plot(sp2, main = '"+ huc + " Subbasin', ylab = 'Number of Species', xlab = 'Collecting Events');"
	theR += "plot(mod1, add=TRUE, col = 2, lwd = 2);"
	theR += "plot(mod2, add=TRUE, col = 3, lwd = 2);"
	theR += "legend('bottomright',c('Lomolino','SSasymp'),fill = c('2','3'));"
	theR += "dev.off();"

	text_file = open('TemporaryR.txt' , 'w')
	text_file.write(theR)
	text_file.close
	subprocess.Popen("Rscript --vanilla D:/Colton_Data/Species_Accumulation/TemporaryR.txt")



#Empty Lists
sighting_dic = {} #Appends taxon onto collecting events
col_keys = [] #Collecting of collecting events
taxon = [] # Taxon
huc8s = [] #HUC8 Key, with collecting event taxon plis





#Creates dataframe with 1 - MRB / 2 - HUC8Name / 3 = Taxon / 4 = Collecting Id
df = pd.read_csv('Data/spaccu.csv', header=None , sep=',')

for row in df.itertuples():
	if row[2] not in huc8s:
		huc8s.append(row[2])

for huc in huc8s:
	#Clears previous list
	taxon.clear()
	col_keys.clear()
	sighting_dic.clear()

	for row in df.itertuples():
		if row[2] == huc: #checks if huc
			if row[3] not in taxon: #Adds unique taxon to list
				taxon.append(row[3])
			if row[4] not in col_keys: #adds unique collecting ids to list
				col_keys.append(row[4])
				sighting_dic.setdefault(row[4],[]) #set key for dict
			sighting_dic[row[4]].append(row[3]) #append tax

	specAccT = {}

	for x in taxon:
		specAccT.setdefault(x,[])
		for y in col_keys:
			if x in sighting_dic[y]:
				specAccT[x].append(1)
			else:
				specAccT[x].append(0)

	
	dataFinal = pd.DataFrame(specAccT)
	count_row = dataFinal.shape[0]

	if count_row > 1:
		dataFinal.to_csv('asym_tables/temp.csv',sep=',')
		runr(huc)
	else:
		print(huc + "is not sampled enough")
	time.sleep(5)