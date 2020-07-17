import os
import sys
from commons import *


for idx in range(0, 4):	
	for x in range(0, 4, 2):
		with open(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv", "r") as resultSourceAnalysis:
			fileLines = resultSourceAnalysis.readlines()

		setEntities = set()

		###Entrazione di tutte le entitita tail e head
		for eachfact in fileLines:
			if len(eachfact) > 2:
				tokenString = eachfact.split(";")
				setEntities.add(tokenString[0])
				setEntities.add(tokenString[2])

		setSrc1 = set()
		setSrc2 = set()

		with open(f"sources/{SOURCES_DATASET[x]}/train.txt", "r") as train1File:
			training1 = train1File.readlines()

		with open(f"sources/{SOURCES_DATASET[x+1]}/train.txt", "r") as train2File:
			training2 = train2File.readlines()

		for eachfactLine in training1:
			if len(eachfactLine) > 2:
				tokenString = eachfactLine.split("\t")
				if tokenString[0] in setEntities or tokenString[2] in setEntities:
					setSrc1.add(f"{tokenString[0]};{tokenString[1]};{tokenString[2]}")

		for eachfactLine in training2:
			if len(eachfactLine) > 2:
				tokenString = eachfactLine.split("\t")
				if tokenString[0] in setEntities or tokenString[2] in setEntities:
					setSrc2.add(f"{tokenString[0]};{tokenString[1]};{tokenString[2]}")

		removedTrainFact = setSrc1.difference(setSrc2)

		with open(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_missingFact.csv", "w") as outputFile:
			for removedFact in sorted(removedTrainFact):
				outputFile.write(f"{removedFact}")
