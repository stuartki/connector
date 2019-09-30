import os
import sys
from Node import Node
from readGrouper import reader
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#topic = raw_input("topic: ")
topic = "diffgeometry"

data = reader(topic)

def axiomer(data):
	axiomList = {}

	count = 0
	for n in data:
		indicate = False
		if count == 0:
			count += 1
			continue
			
			
		for l in n.past:
			if l == '':
				indicate = True
			else:
				indicate = False
		
		c = 0
		for x in n.future:
			if x == '':
				continue
			else:
				c +=1				
				
		if indicate:
			axiomList[n.title] = c

	return axiomList

d = data[6].description
words = word_tokenize(d)


stop_words = set(stopwords.words('english'))

fs = [w for w in words if not w.lower() in stop_words]
f = set(fs)

for x in data:
	if isinstance(x, int):
		continue
	if x.title in f:
		print x.title + ": " + x.id
