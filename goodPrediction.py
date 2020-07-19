import os
from commons import *


goodExample = []

counterGlobal = 0
for idx in range(0, 4):	
	for x in range(0, 4, 2):

		if not os.path.exists(f"output/good_prediction"):
			os.makedirs(f"output/good_prediction", exist_ok=True)


		dt1 = readFile(f"sources/{SOURCES_DATASET[x]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv")
		dt2 = readFile(f"sources/{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv")


		countLocal = 0
		for line in dt2:
			tokenLine = line.split(";")
			try:
				head_r = int(tokenLine[3])
				tail_r = int(tokenLine[4])
				if head_r == 1 and tail_r == 1 and not "." in line:
					goodExample.append(line)

					with open(f"sources/{SOURCES_DATASET[x+1]}/train.txt", "r") as trainFile:
						trainHead = set()
						trainTail = set()

						lines_t = trainFile.readlines()
						for line_t in lines_t:
							tokenLine_t = line_t.replace("\n", "")
							tokenLine_t = tokenLine_t.split("\t")
							if tokenLine_t[0] == tokenLine[0] or tokenLine_t[2] == tokenLine[0]:
								trainHead.add(tokenLine_t[0])
								trainHead.add(tokenLine_t[2])
							if tokenLine_t[0] == tokenLine[2] or tokenLine_t[2] == tokenLine[2]:
								trainTail.add(tokenLine_t[0])
								trainTail.add(tokenLine_t[2])
					print(countLocal, tokenLine)
					commonEnt = trainHead.intersection(trainTail)
					print(commonEnt)
					if len(commonEnt) > 0:
						counterGlobal += 1
					countLocal += 1
					if countLocal > 20: 
						break
			except:
				continue

print(f"{counterGlobal}/{len(goodExample)} founded with path 2")
with open("output/good_prediction/result.txt", "w") as rsFile:
	for ex in goodExample:
		rsFile.write(ex)

