import os
import sys
from Node import Node
from reader import reader
import json
from searcher import ls, searcher, get
from writer import isint

def writeToFile(file, data):
	open(file, "w").close()
	data= data[1:]
	data = [n.__dict__ for n in data]
	with open(file, "w") as current_file:
		current_file.write(json.dumps(data))

def edit(data):

	
	content = ""
	
	while content != "end":
		content = input("id: ")
		
		if content == "end":
			continue
		if content[:2] == "ls":
			ls(content, data)
			continue

		if content == "search":
			se = ""
			while se != "end":
				se = input("search: ")
				if se == "end":
					continue
				if isint(se):
					from mapper import reload
					get(data, reload(data), id = int(se))
				for n in searcher(se, data):
					print(str(n.id) + ": " + n.title)
		try:
			id = int(content)
		except ValueError:
			print("INVALID ID")
			continue
		
		cur_node = data[id]
		cur = ""
		while cur != "end":
			cur = input(str(id) + ": ")
			if cur == "end":
				continue
			if cur == "ls":
				cur_node.printNode()
			if cur == "description":

				new_descr = input("\n" + str(id) + ".description: " + str(cur_node.description) + "\n")
				if new_descr == "end":
					continue
				else:
					if "+a" == cur[:-2]:
				 		new_descr = cur_node.description + ". " + new_descr
					cur_node.description = new_descr
					print("\n" + str(id) + ".description: " + str(cur_node.description) + "\n")
			if cur == "past":
				p = ""
				print("\npast: " + str(cur_node.past) + "\n")
				while p != "end":

					p = input()
					if p == "end":
						continue
					if p[:2] == "ls":
						print("\npast: " + str(cur_node.past) + "\n")
						ls(p, data)
						continue
					
					if p == "search":
						se = ""
						while se != "end":
							se = input("search: ")
							if se == "end":
								continue
							if isint(se):
								from mapper import reload
								get(data, reload(data), id = int(se))
							for n in searcher(se, data):
								print(str(n.id) + ": " + n.title)
					try:
						ind = p[0]
						newID = int(p[1:])
					except:
						print("INVALID ID")
						p = input("\npast: " + str(cur_node.past) + "\n")
						continue
					
					if ind == "-":
						cur_node.past.remove(newID)
						data[newID].future.remove(id)
					if ind == "+":
						cur_node.past.append(newID)
						data[newID].future.append(id)
			if cur == "future":

				p = ""
				print("\nfuture: " + str(cur_node.future) + "\n")
				while p != "end":

					p = input()
					if p == "end":
						continue
					if p[:2] == "ls":
						print("\nfuture: " + str(cur_node.future) + "\n")
						ls(p, data)
						continue
					
					if p == "search":
						se = ""
						while se != "end":
							se = input("search: ")
							if se == "end":
								continue
							if isint(se):
								from mapper import reload
								get(data, reload(data), id = int(se))
							for n in searcher(se, data):
								print(str(n.id) + ": " + n.title)
					try:
						ind = p[0]
						newID = int(p[1:])
					except:
						print("INVALID ID")
						p = input("\nfuture: " + str(cur_node.future) + "\n")
						continue
					
					if ind == "-":
						cur_node.future.remove(newID)
						data[newID].past.remove(id)
					if ind == "+":
						cur_node.future.append(newID)
						data[newID].past.append(id)
			if cur == "related":
				pa = ""
				while pa != "end":

					pa = input("\nid: " + str(id) + "\n" + ", ".join(cur_node.related) + "\n\n: ")
					if pa == "end":
						continue
					
					p = list(pa)
					if p[0] == "-":
						cur_node.related.remove(p[1])
						data[int(p[1])].related.remove(p[1])
					if p[0] == "+":
						cur_node.related.append(p[1])
						data[int(p[1])].related.append(p[1])
					print("\nid: " + str(id) + "\n" + ", ".join(cur_node.related))
			if cur == "keywords":

				pa = ""
				while pa != "end":

					pa = input("\nid: " + str(id) + "\n" + ", ".join(cur_node.keywords) + "\n\n: ")
					if pa == "end":
						continue
					
					p = list(pa)
					if p[0] == "-":
						cur_node.keywords.remove(p[1])
					if p[0] == "+":
						cur_node.keywords.append(p[1])	
					print("\nid: " + str(id) + "\n" + ", ".join(cur_node.keywords))
			if "title" in cur:
				
				titleNew = input("\n" + str(id) + ".title: " + cur_node.title + "\n")
				if titleNew == "end":
					continue
				else:
					if "+a" == cur[:-2]:
						titleNew = cur_node.title + ". " + titleNew
					cur_node.title = titleNew	
				print("\n" + str(id) + ".title: " + cur_node.title + "\n")
# 			if cur == "type":
# 
# 				typeNew = input("\nid: " + str(id) + "\n" + cur_node.type + "\n\n: ")
# 				if descrNew == "end":
# 					continue
# 				else:
# 					cur_node.description = descrNew	
# 				print "\nid: " + str(id) + "\n" + cur_node.type
				
	return data
				