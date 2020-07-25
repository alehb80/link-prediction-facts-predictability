import os
from commons import *



for idx in range(0, 4):	
	for x in range(0, 4, 2):

		if not os.path.exists(f"output/good_prediction"):
			os.makedirs(f"output/good_prediction", exist_ok=True)

		goodExample = []
		counterGlobal = 0
		#dt1 = readFile(f"sources/{SOURCES_DATASET[x]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv")
		#dt2 = readFile(f"sources/{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv")
		dt2 = readFile(f"output/{SOURCES_DATASET[x]}-{SOURCES_DATASET[x+1]}/{MODELS_NAME[idx]}/{MODELS_NAME[idx].lower()}_filtered_ranks.csv")

		with open(f"sources/{SOURCES_DATASET[x+1]}/train.txt", "r") as trainFile:
			lines_t = trainFile.readlines()


		countLocal = 0
		for line in dt2:
			tokenLine = line.replace("\n", "").split(";")
			try:
				head_r = int(float(tokenLine[3]))
				tail_r = int(float(tokenLine[4]))
				#if head_r == 1 and tail_r == 1 and not "." in tokenLine[1]:
				if not "." in tokenLine[1]:
					goodExample.append(line)

					
					trainHead = set()
					trainTail = set()

						
					for line_t in lines_t:
						tokenLine_t = line_t.replace("\n", "")
						tokenLine_t = tokenLine_t.split("\t")
						if tokenLine_t[0] == tokenLine[0] or tokenLine_t[2] == tokenLine[0]:
							trainHead.add(tokenLine_t[0])
							trainHead.add(tokenLine_t[2])
						if tokenLine_t[0] == tokenLine[2] or tokenLine_t[2] == tokenLine[2]:
							trainTail.add(tokenLine_t[0])
							trainTail.add(tokenLine_t[2])
					#print(countLocal, tokenLine)
					commonEnt = trainHead.intersection(trainTail)
					#print(commonEnt)
					if len(commonEnt) > 0:
						counterGlobal += 1
					countLocal += 1
					if countLocal >= 100: 
						break
			except:
				continue
		print(f"[{SOURCES_DATASET[x+1]} - {MODELS_NAME[idx]}]{counterGlobal}/{len(goodExample)} --> {counterGlobal}%")
		print("#############")


#with open("output/good_prediction/result.txt", "w") as rsFile:
	#for ex in goodExample:
		#rsFile.write(ex)

