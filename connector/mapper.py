import os
import sys
from Node import Node
from reader import reader
from searcher import searcher, get, isCycle, ls
from writer import writer, isint
from edit import edit
from writer import writeToFile
from network import mostPopularSuc, mostPopularPred, init, draw_all, cleanPred, most_degree_centrality, labeler
import json
import networkx as nx
import matplotlib.pyplot as plt
from projecter import get_project, print_graph, branch




def reload(data):
	DG = init(data)
	#clean graph initially
	DG = cleanPred(data, DG)
	return DG
	
def interface(init_topic = ""):
	from mapper import reload
	topic = ""
	while topic != "end":
		#loading topic
		if init_topic == "":
			topic = input("topic: ")
			
			if topic == "end":
				continue
			if topic == "ls":
				for n in [n.replace(".json", "") for n in os.listdir("../data/") if ".json" in n]:
					print(n)
				continue
			if len(searcher(topic, list(os.listdir("../data/")))) > 0:
				print()
				for n in [n.replace(".json", "") for n in searcher(topic, list(os.listdir("../data/"))) if ".json" in n]:
					print(n)
		else:
			topic = init_topic
		file = "../data/" + topic + ".json"

		if topic + ".json" not in set(os.listdir("../data/")):
			print("NEW")
			conf = input("confirm: ")
			#need a confirm option
			if conf == "y" or conf == "yes":
				with open(file, "w+") as cur_file:
					cur_file.write(json.dumps([]))
			else:
				continue
		
		start = ""
		data = reader(topic)
		DG = reload(data)
		#for the purpose of recording changes to length of dataset
		preLen = len(data)
		path = ""
		walker = 0
		SET_OF_COMMANDS = ["end", "print", "edit", "write", "search"]
		#actions
		while start != "end":
			start = input(topic + ": ")
			if start == "end":
				continue

			#print the new data? useless method because it writes to file everytime
			if start == "print":
				for i in range(preLen + 1, len(data)):
					print(str(data[i].id) + ": " + data[i].title)
					
				print(data)
				conf = input("confirm?: ")
				if conf == "y" or conf == "yes":
					writeToFile(file, data)
				else:
					continue

			if start == "edit":
				data = edit(data)
				writeToFile(file, data)
				DG = reload(data)

			#WRITING CONTENT
			if start == "write":
				writer(topic)
				data = reader(topic)
				DG = reload(data)
			
			if start == "search":
				se = ""
				while se != "end":
					if se == "end":
						continue
					se = input("search: ")
					for n in searcher(se, data):
						print(str(n.id) + ": " + n.title)

			if isint(start):
				get(data, DG, id = int(start))

			if start[:2] == "ls":
				ls(start, data)
				continue
				
			if start == "graph":
				draw_all(data, DG)
				
			#summarize data
			#degree centrality, pred nodes, suc nodes (page rank)
			if start == "summarize":
				size = int(len(DG.nodes())/10)
				print("Size = " + str(size)) 
				centralnodes =  [n[0] for n in most_degree_centrality(DG, limit = size)]
				
				suc = mostPopularSuc(data, DG, limit = size)
				pred = mostPopularPred(data, DG, limit = size)
				
				totalNodes = []
				totalNodes.extend(centralnodes)
				totalNodes.extend(suc)
				totalNodes.extend(pred)
				
				print("Pred Nodes: ")
				print()
				for n in pred:
					print(str(n.id) + ": " + str(n.title))
				print()
				print("Central Nodes: ")
				print()
				for n in centralnodes:
					print(str(n.id) + ": " + str(n.title))
				print()
				print("Suc Nodes: ")
				print()
				for n in suc:
					print(str(n.id) + ": " + str(n.title))

				
				
				p = input("plot? ")
				if p == "y" or p == "yes":
					subDG = DG.subgraph(totalNodes)
					labels = labeler(data)
					pos = nx.spring_layout(subDG)
					labelDict = {n:lab for n,lab in labels.items() if n in pos}
					nx.draw(subDG, pos, with_labels = True, font_size = 12, labels = labelDict)
					plt.draw()
					plt.show()

			if start == "get":
				get(data, DG)

			if start == "cycle":
				isCycle(DG)
				
			if start == "project":
				get_project(data, DG)

			if start == "branch":
				branch(data, DG)
			
			if start == "pyvis":
				from net_vis import net_vis
				net_vis(data)
			
			if start == "load":
				from load import file_finder, term_text_editor, pdf_loader, txt_loader
				if len(path) > 0:
					s = input("LOADED PATH: " + path + "\n")
					if s == "new":
						path = file_finder()
						if ".txt" in path:
							t_data = txt_loader(path)
						elif ".pdf" in path:
							t_data = pdf_loader(path)
						else:
							print("NO VALID FILE")
						term_text_editor(path, from_topic = topic)
						data = reader(topic)
						DG = reload(data)
					else:
						walker = term_text_editor(t_data , init_index = walker, from_topic= topic)
						data = reader(topic)
						DG = reload(data)
				else:
					path = file_finder()
					if ".txt" in path:
						t_data = txt_loader(path)
					elif ".pdf" in path:
						t_data = pdf_loader(path)
					else:
						print("NO VALID FILE")
					walker = term_text_editor(t_data, from_topic = topic)
					data = reader(topic)
					DG = reload(data)

if __name__ == "__main__":
	interface()
			
