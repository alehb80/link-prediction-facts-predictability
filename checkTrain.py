import os


class entity:

	def __init__(self, name, pos):
		self.name = name
		self.pos_dist = 0
		self.fact = []

	def setFact(fact):
		self.fact = fact

class Fact:
	def __init__(self, header, relation, tail, dist):
		self.header = header
		self.relation = relation
		self.tail = tail
		self.dist = dist

	def __str__(self):
		return f"{self.header} {self.relation} {self.tail}"

	def __eq__(self, other):
		return self.header == other.header and self.relation == other.relation and self.tail == other.tail

	def __hash__(self):
		return hash((self.header,self.relation, self.tail))


entityExplored = []
entityCollection = [Fact("/m/0jgxn", "/film/film_subject/films", "/m/0c57yj", 0)]

with open("sources/FB15k-237/train.txt", "r") as trainFile:
	trainLines = trainFile.readlines()

def SearchFactForEntities(entity_name, dist):
	print(f"Searching {entity_name}")
	fact = []
	for line in trainLines:
		tokenLine = line.replace("\n", "")
		tokenLine = tokenLine.split("\t")
		if entity_name == tokenLine[0] or entity_name == tokenLine[2]:
			fact.append(Fact(tokenLine[0], tokenLine[1], tokenLine[2], dist))
	return fact



distance = 0

while len(entityCollection) > 0:
	currFact = entityCollection.pop(0)
	###############
	print("Searching From", currFact)
	if currFact.dist > 2:
		print("Stopping Because Too Deep")
		break
	headFacts = set(SearchFactForEntities(currFact.header, currFact.dist +1))
	if len(headFacts) < 1:
		print("Stopping Because Head No Data")
		continue
	tailFacts = set(SearchFactForEntities(currFact.tail, currFact.dist +1))
	if len(tailFacts) < 1:
		print("Stopping Because Tail No Data")
		continue
	print(f"Founded HFact:{len(headFacts)},  TFact:{len(tailFacts)}")
	entityCollection = entityCollection + list(headFacts.union(tailFacts))


for fact in set(sorted(entityCollection, key=lambda val: val.tail)):
	print(fact.header, fact.relation, fact.tail, fact.dist)





