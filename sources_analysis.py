import os
import sys


SOURCES_DATASET = ["FB15k", "FB15k-237", "WN18", "WN18RR"]
MODELS_NAME = ["AnyBURL-RE", "ComplEx", "HAKE", "InteractE"]


def readFile(filePath):
	with open(filePath, "r") as fileStream:
		lines = fileStream.readlines()
	return lines


for idx in range(0, 4):	
	for x in range(0, 4, 2):

		if not os.path.exists(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}"):
			os.makedirs(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}", exist_ok=True)


		dt1 = readFile(f"sources/{SOURCES_DATASET[x]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv")
		dt2 = readFile(f"sources/{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv")


		array_result_diff = []
		array_result_nofound = []

		workDict = {}


		for line in dt1:			
			tokenRow = line.split(";")
			if len(tokenRow) > 3:
				keyString= "".join(tokenRow[:3])
				workDict[keyString] = { "dc1" : tokenRow, "counter":1}
			

		for line in dt2:
			tokenRow = line.split(";")
			if len(tokenRow) > 3:
				keyString= "".join(tokenRow[:3])
				if keyString in workDict.keys():
					workDict[keyString]["dc2"] = tokenRow
					workDict[keyString]["counter"] += 1
				else:
					array_result_nofound.append(tokenRow)

		###Introduco la Policy per selezionare i differenti

		for key, value in workDict.items():
			if value["counter"] > 1:
				isImproved=True
				diff_h = 0
				diff_t = 0

				#Da numero passato a digit allora peggiora
				if value["dc1"][3].replace(".", "").isdigit() and not value["dc2"][3].replace(".", "").isdigit():
					isImproved = False

				if value["dc1"][4].replace(".", "").isdigit() and not value["dc2"][4].replace(".", "").isdigit():
					isImproved = False

				#Confronto tra numeri
				if value["dc1"][3].replace(".", "").isdigit() and value["dc2"][3].replace(".", "").isdigit():
					diff_h = float(value["dc1"][3]) -  float(value["dc2"][3])

				if value["dc1"][4].replace(".", "").isdigit() and value["dc2"][4].replace(".", "").isdigit():
					diff_t = float(value["dc1"][4]) -  float(value["dc2"][4])

				if not isImproved or diff_h > 0 or diff_t > 0:
					array_result_diff.append( {"head" : value["dc1"][0], "relation" : value["dc1"][1], "tail" : value["dc1"][2], "head_rank_d" : diff_h, "tailt_rank_d" : diff_t, "founded" : isImproved})


		with open(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv", "w") as outputFile:
			for fact in array_result_diff:
				outputFile.write(f"{fact['head']};{fact['relation']};{fact['tail']};{fact['head_rank_d']};{fact['tailt_rank_d']};{fact['founded']}\n")
				

