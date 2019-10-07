#writer
#v4
#what if we parse the description for keywords?

#INPUT: name of the file, list of Nodes

import os
import sys
from Node import Node
from reader import reader
from edit import edit
from searcher import searcher, ls
import json
from network import mostPopularSuc, mostPopularPred, init,	draw_all, cleanPred, most_degree_centrality, labeler
from projecter import get_project, print_graph, branch
def isint(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def writeToFile(file, data):
	open(file, "w").close()
	#leaves open for max
	data= data[1:]
	data = [n.__dict__ for n in data]
	with open(file, "w") as current_file:
		current_file.write(json.dumps(data))

def writer(topic, data = 0, init_description = ""):
	from writer import writeToFile, isint

	
	#cleaning function making sure each node is properly linked
	def clean(data, curNode):
		for n in curNode.future:
			if n >= len(data):
				continue
			pastArray = data[n].past
			if n not in pastArray:
				data[n].flashback(curNode.id)
		for n in curNode.past:
			if n >= len(data):
				continue
			futureArray = data[n].future
			if n not in futureArray:
				data[n].flashforward(curNode.id)
		for n in curNode.related:
			if n >= len(data):
				continue
			relatedArray = data[n].related
			if n not in relatedArray:
				data[n].relate(curNode.id)
	
	file = "../data/" + topic + ".json"

	data = reader(topic)
	DG = init(data)
	DG = cleanPred(data, DG)
	max = len(data)


	content = ""
	summary = init_description
	print(topic + ".write: " + summary)
	
	
	while content != "end":
		content = input("")
		
		if content == "end":
			continue
		#summary function
		if content == "ls":
			print(summary)
			continue
		#enter
		if content == "\n":
			summary += "\n"
			continue
		#premature break
		if content == "break":
			break
		#writing the actual content		
		summary += content + " "
	
	#premature break
	if content == "break":
		return ""
	#connecting the content
	
	#get title
	print("Title: ")
	title = input("")
	if title == "up":
		title = summary
	
	print("Type: ")
	type = []
	t = ""
	while t != "end":
		t = input("")
		if t == "end":
			continue
		type.append(t)
	
	print("Past: ")
	past_temp = ""
	back = []
	while past_temp != "end":
		past_temp  = input("")
		if past_temp == "end":
			continue
		if past_temp[:2] == "ls":
			ls(past_temp, data)
			continue
		if past_temp == "suc":
			for n in mostPopularSuc(data, DG, limit = 10):
				print(str(n.id) + ": " + n.title)
			continue
		if past_temp == "pre":
			for n in mostPopularPred(data, DG, limit = 10):
				print(str(n.id) + ": " + n.title)
			continue
		if past_temp == "cen":
			for n in most_degree_centrality(DG, limit = 10):
				print(str(n[0].id) + ": " + n[0].title)
			continue
		if past_temp == "project":
			get_project(data, DG)
		if past_temp == "branch":
			branch(data, DG)
		if isint(past_temp):
			result = int(past_temp)
			back.append(result)
		else:
			print([str(n.id) + ": " + str(n.title) for n in searcher(past_temp, data)])
		print(back)

	print("Future: ")
	future_temp = ""
	future = []
	while future_temp != "end":
		future_temp  = input("")
		if future_temp == "end":
			continue
		if future_temp[:2] == "ls":
			try:
				l = int(future_temp[2:])
				if l > len(data):
					l = len(data)
			except:
				l = len(data)
			for n in range(len(data)-l, len(data)):
				if isinstance(data[n], int):
					continue
				print(str(data[n].id) + ": " + str(data[n].title))
			continue
		if future_temp == "suc":
			for n in mostPopularSuc(data, DG, limit = 10):
				print(str(n.id) + ": " + n.title)
		if future_temp == "pre":
			for n in mostPopularPred(data, DG, limit = 10):
				print(str(n.id) + ": " + n.title)
		if future_temp == "cen":
			for n in most_degree_centrality(DG, limit = 10):
				print(str(n[0].id) + ": " + n[0].title)
		if isint(future_temp):
			result = int(future_temp)
			future.append(result)
		else:
			print([str(n.id) + ": " + str(n.title) for n in searcher(future_temp, data)])
		print(future)
	
	#simplify things, break things up into if you want to add related
	c = ""
	related = []
	keyword = []
	while c != "end":
		c = input("")
		if c == "end":
			continue
		if c == "break":
			break
		#if you want to add related
		if c == "related":
			print("Related: ")
			r_temp = ""
			while r_temp != "end":
				r_temp  = input("")
				if r_temp == "end":
					continue
				if isint(r_temp):
					result = int(r_temp)
					related.append(result)
				else:
					print([str(n.id) + ": " + str(n.title) for n in searcher(r_temp, data)])
				print(related)
		#if you want to add keywords
		if c == "keywords":
			print("Keywords: ")
			k_temp = ""
			while k_temp != "end":
				k_temp  = input("")
				if k_temp == "end":
					continue
				keyword.append(k_temp)
		if c == "edit":
			data = edit(data)
	if c == "break":
		return ""
	print(title)
	print(type)
	print(summary)
		
	#CLEANING
	
	current_Node = Node(title, type, summary, keyword, back, future, related, max)
	clean(data, current_Node)
	data.append(current_Node)
	max += 1
	
	#WRITING BACK TO TXT FILE
	writeToFile(file, data)
			

			
			
		

