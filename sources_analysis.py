import os
import sys
from commons import *



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

				if value["dc1"][3].startswith("MISS"):
					value["dc1"][3] = str(rankMissValue(value["dc1"][3], DATASET_ENTITIES[x]))

				if value["dc1"][4].startswith("MISS"):
					value["dc1"][4] = str(rankMissValue(value["dc1"][4], DATASET_ENTITIES[x]))

				if value["dc2"][3].startswith("MISS"):
					value["dc2"][3] = str(rankMissValue(value["dc2"][3], DATASET_ENTITIES[x+1]))

				if value["dc2"][4].startswith("MISS"):
					value["dc2"][4] = str(rankMissValue(value["dc2"][4], DATASET_ENTITIES[x+1]))


				#Confronto tra numeri
				if value["dc1"][3].replace(".", "").isdigit() and value["dc2"][3].replace(".", "").isdigit():
					diff_h = int(float(value["dc1"][3])) -  int(float(value["dc2"][3]))

				if value["dc1"][4].replace(".", "").isdigit() and value["dc2"][4].replace(".", "").isdigit():
					diff_t = int(float(value["dc1"][4])) -  int(float(value["dc2"][4]))

				if (diff_h < 0  or diff_t < 0) and int(float(value["dc1"][3])) == 1 and int(float(value["dc1"][4])) == 1:
					array_result_diff.append( {"head" : value["dc1"][0], "relation" : value["dc1"][1], "tail" : value["dc1"][2], "head_rank_d" : diff_h, "tail_rank_d" : diff_t , "sumdiff" : diff_h + diff_t})

		sortedresultSum = sorted(array_result_diff, key=lambda val: float(val['sumdiff']))
		sortedresultHead = sorted(array_result_diff, key=lambda val: float(val['head_rank_d']))
		sortedresultTail = sorted(array_result_diff, key=lambda val: float(val['tail_rank_d']))

		with open(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv", "w") as outputFile:
			index = 0
			for fact in sortedresultSum:
				if index < 3:
					if not "." in fact['relation']:
						outputFile.write(f"{fact['head']};{fact['relation']};{fact['tail']};{fact['head_rank_d']};{fact['tail_rank_d']};{fact['sumdiff']}\n")
						index += 1
				else:
					break

		with open(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranksh.csv", "w") as outputFile:
			index = 0
			for fact in sortedresultHead:
				if index < 3:
					if not "." in fact['relation']:
						outputFile.write(f"{fact['head']};{fact['relation']};{fact['tail']};{fact['head_rank_d']};{fact['tail_rank_d']};{fact['sumdiff']}\n")
						index += 1
				else:
					break

		with open(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_rankst.csv", "w") as outputFile:
			index = 0
			for fact in sortedresultTail:
				if index < 3:
					if not "." in fact['relation']:
						outputFile.write(f"{fact['head']};{fact['relation']};{fact['tail']};{fact['head_rank_d']};{fact['tail_rank_d']};{fact['sumdiff']}\n")
						index += 1
				else:
					break
				

