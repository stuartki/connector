
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

def ls(i, data, limit = -1):
	if limit > 0:
		l = limit
	else:
		try: 
			l = int(i[2:])
		except:
			l = int(15)
	if l > len(data):
		l = len(data)
	for n in range(len(data)-l, len(data)):
		if isinstance(data[n], int):
			continue
		print(str(data[n].id) + ": " + str(data[n].title))

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

def get(data, DG, id = -1):
	from projecter import print_graph
	if id < 0:
		id = input("id: ")
	
	try:
		id = int(id)
		print(data[id].description)
		s = set([data[id]])
		for n in data[id].future:
			s.add(data[n])
		for n in data[id].past:
			s.add(data[n])
		
		print_graph(DG.subgraph(list(s)), unique=True)
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
def searcher(word, data, index = False):
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
					if index:
						returnArray.append(data.index(item))
					else:
						returnArray.append(item)
					break
		elif isinstance(item, str):
			for w in ngram(item, n):
				if word in w.lower():
					if index:
						returnArray.append(data.index(item))
					else:
						returnArray.append(item)
					break
			
			
		
	return returnArray
	

