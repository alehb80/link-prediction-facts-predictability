SOURCES_DATASET = ["FB15k", "FB15k-237", "WN18", "WN18RR"]
MODELS_NAME = ["AnyBURL-RE", "ComplEx", "HAKE", "InteractE"]
DATASET_ENTITIES = [14951, 14541, 40943, 40943]


def readFile(filePath):
	with open(filePath, "r") as fileStream:
		lines = fileStream.readlines()
	return lines

def rankMissValue(strValue, entitiesNumber):
	value = int(strValue[strValue.find("_")+1:])
	return float((value + entitiesNumber) / 2)