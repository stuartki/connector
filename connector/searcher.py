
import os
import sys
from Node import Node
import networkx as nx
	
# def pastNode(content, data):
# 	pastNodes = []
# 	words = word_tokenize(content)


# 	stop_words = set(stopwords.words('english'))

# 	fs = [w for w in words if not w.lower() in stop_words]
	
# 	f = list(set(fs))

# 	for x in data:
# 		if isinstance(x, int):
# 			continue
# 		if x.title in f:
# 			pastNodes.append(x.id)
# 	return pastNodes

def ngram(phrase, n):
	phrase = phrase.split(' ')
	output = []
	for i in range(len(phrase)-n+1):
		f = ""
		for s in phrase[i:i+n]:
			f += s + ' '
			
		f = f[:-1]
		output.append(f)
	return output

def get(data):
	id = input("id: ")
	try:
		id = int(id)
		data[id].printNode()
	except:
		print("NOT INT")
		
def isCycle(DG):
	try:
		cycle = nx.find_cycle(DG)
		for edge in cycle:
			n = edge[0]
			print(str(n.id) + ": " + n.title)
	except:
		print("NO CYCLES")

#search generically if the word is in data (type list) 
def searcher(word, data):
	def ngram(phrase, n):
		phrase = phrase.split(' ')
		output = []
		for i in range(len(phrase)-n+1):
			f = ""
			for s in phrase[i:i+n]:
				f += s + ' '
			
			f = f[:-1]
			output.append(f)
		return output
	word = word.lower()
	n = len(word.split(' '))
	returnArray = []
	
	for item in data:
		if isinstance(item, Node):
			for w in ngram(item.title, n):
				if word in w.lower():
					returnArray.append(item)
					break
		elif isinstance(item, str):
			for w in ngram(item, n):
				if word in w.lower():
					returnArray.append(item)
					break
			
			
		
	return returnArray
	

