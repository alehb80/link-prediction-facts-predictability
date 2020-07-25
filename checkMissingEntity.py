import os
from commons import *

for idx in range(0, 4):	
	for x in range(0, 4, 2):
		with open(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv", "r") as badPredictionFile:

			fileEntities = set()
			trainEntities = set()

			entityDictionary = {}

			lines = badPredictionFile.readlines()

			for factRank in lines:
				if len(factRank) > 2:
					tokenString = factRank.split(";")
					fileEntities.add(tokenString[0])
					fileEntities.add(tokenString[2])



		
		with open(f"sources/{SOURCES_DATASET[x+1]}/train.txt", "r") as trainFile:

			trainlines = trainFile.readlines()

			for factTrain in trainlines:
				if len(factTrain) > 2:
					tokenString = factTrain.replace("\n", "").split("\t")
					trainEntities.add(tokenString[0])
					trainEntities.add(tokenString[2])

					if not tokenString[0] in entityDictionary.keys():
						entityDictionary[tokenString[0]] = { "counter" : 0 }

					if not tokenString[2] in entityDictionary.keys():
						entityDictionary[tokenString[2]] = { "counter" : 0 }

					entityDictionary[tokenString[0]]['counter'] += 1
					entityDictionary[tokenString[2]]['counter'] += 1

			missingEntity = fileEntities.difference(trainEntities)

			factMissArrayCount = 0

			print(f"[{SOURCES_DATASET[x+1]}] Train Entities Founded : {len(trainEntities)}")
			print(f"[{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}][{MODELS_NAME[idx].lower()}]Entity Founded : {len(fileEntities)}")
			print(f"Missing Entities in training: {len(missingEntity)}")
			

			with open(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranksWithLink.csv", "w") as linkObjectFile:
				counterDisProp = 0
				counterProp = 0
				for factRank in lines:
					if len(factRank) > 2:
						tokenString = factRank.split(";")
						head = tokenString[0]
						tail = tokenString[2]

						currentFact = factRank.replace('\n', '')

						if head in missingEntity or tail in missingEntity:
							factMissArrayCount += 1
							continue
						entityKeys = entityDictionary.keys()
						if head in entityKeys and tail in entityKeys:
							linkObjectFile.write(f"{currentFact};{entityDictionary[head]['counter']};{entityDictionary[tail]['counter']}\n")
							maxCount = max(entityDictionary[head]['counter'], entityDictionary[tail]['counter'])
							minCount = min(entityDictionary[head]['counter'], entityDictionary[tail]['counter'])
							###Verifico se train sproporzionato e la sproporzione influisce sul fallimento
							if (minCount/maxCount) * 100 <= 25:
								if (minCount == entityDictionary[head]['counter'] and min(int(tokenString[3]), int(tokenString[4])) == int(tokenString[3])) or (minCount == entityDictionary[tail]['counter'] and min(int(tokenString[3]), int(tokenString[4])) == int(tokenString[4])):
									counterDisProp += 1
								else:
									counterProp += 1
						elif  head in entityKeys and not tail in entityKeys:
							linkObjectFile.write(f"{currentFact};{entityDictionary[head]['counter']};0\n")
						elif not head in entityKeys and tail in entityKeys:
							linkObjectFile.write(f"{currentFact}; 0;{entityDictionary[tail]['counter']}\n")
						else:
							linkObjectFile.write(f"{currentFact}; 0;0\n")

			print(f"Missing Entities Facts in test : {factMissArrayCount}")
			print(f"Disproportion head tail in train : {counterDisProp} of {counterDisProp+counterProp}  --> {(counterDisProp/(counterDisProp+counterProp))*100}%")
			print("#########################################")


