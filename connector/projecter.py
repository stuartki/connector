import networkx as nx
import os
import sys
from Node import Node
import matplotlib.pyplot as plt
import operator
from collections import Counter, defaultdict
import pandas as pd



def print_graph(DG, unique = False):
	totcount = 0
	marked = set()
	def bfsP(node, tab = ""):
		count = 0
		marked.add(node)
		print(tab + str(node.id) + ": " + node.title)
		count +=1
		tab += "\t"
		for n in DG.successors(node):
			
			if n not in marked:
				count+=bfsP(n,  tab = tab)
			elif not unique:
				print(tab + str(n.id) + ": " + n.title)
				count+=1
		return count


	
	axioms = [n for n,d in DG.in_degree() if d == 0]
	

	for node in axioms:
		totcount += bfsP(node)
		print()
	return totcount
		
def get_project(data, DG, unique = False):
	leaves = [n for n,d in DG.out_degree() if d == 0]
	roots = [n for n,d in DG.in_degree() if d == 0]
	dict = {}
	c = ""
	back = False
	while c != "end":
		c= input("project: ")
		if c == "end":
			continue
		if c == "unique" or c == "u":
			unique = True
		if c == "!u" or c == "!unique":
			unique = False
		in_id = input("InID: ")
		out_id = input("OutID: ")
		
		if in_id == "all" and out_id == "all":

			for node in roots:
				s = set()
				for out in leaves:
					try:
						for a in nx.all_simple_paths(DG, node, out):
							for b in a:
								s.add(b)
					except:
						continue

				dict[node] = DG.subgraph(s)
		
		elif out_id == "all" and in_id != "all":
			while True:
				try:
					in_id = int(in_id)
				except ValueError:
					print("INVALID IN_ID")
					back = True
					break

				else:
					break
			if back:
				continue

			in_node = data[in_id]
			s = set()
			for out in leaves:
				try:
					for a in nx.all_simple_paths(DG, in_node, out):
						for b in a:
							s.add(b)
				except:
					continue

				dict[in_node] = DG.subgraph(s)
		elif in_id == "all" and out_id != "all":
			while True:
				try:
					out_id = int(out_id)
				except ValueError:
					print("INVALID OUT_ID")
					back = True
					break

				else:
					break
			if back:
				continue

			out_node = data[out_id]
			s = set()
			for p in roots:
				try:
					for a in nx.all_simple_paths(DG, p, out_node):
						for b in a:
							s.add(b)
				except:
					continue

			dict[p] = DG.subgraph(s)

		else:
			while True:
				try:
					out_id = int(out_id)
					in_id = int(in_id)
				except ValueError:
					print("INVALID ID")
					back = True
					break

				else:
					break
			if back:
				continue

			out_node = data[out_id]
			in_node = data[in_id]
			s = set()

			try:
				for a in nx.all_simple_paths(DG, in_node, out_node):
					for b in a:
						s.add(b)
			except:
				print("NO PATH")
			
			dict[in_node] = DG.subgraph(s)

		total_set = set()
		if unique:
			total_set = set([m for n in dict.values() for m in n.nodes()])
			subG = DG.subgraph(total_set)
			print_graph(subG)
		else:
			for n in dict.keys():
				if len(dict[n].nodes()) != 0:
					print_graph(dict[n])
					total_set.union([n for n in dict[n].nodes()])
		pl = input("plot: ")
		if pl == "y" or pl == "yes":
			nx.draw(DG.subgraph(total_set))
			plt.show()
		
	return dict


def branch(data, DG, rec = []):
	
	# from networkx.algorithms import community
	s = ""
	while s != "end":
		s = input("branch: ")
		if s == "end":
			continue
		if s == "louvain":
			import community as louvain
			louv = input("louvain: ")
			G = DG.to_undirected()
			partition = louvain.best_partition(G)
			if louv == "iter":
				# if len(rec) > 0:
				# 	rec_limit = set([partition[data[k]] for k in rec])
				# else: 
				# 	rec_limit = 0
				for com in set(partition.values()):
					i = input()
					if i == "end":
						break
					print("COMMUNITY NUMBER " + str(com+1))
					list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
					print_graph(DG.subgraph(list_nodes), unique = True)

			if louv == "all":
				#undirected graph community detection
				totcount = 0
				pos = nx.spring_layout(G.to_undirected())
				size = float(len(set(partition.values())))
				def print_community(com_dict, G, plot = False):
					count = 0.
					c = 0.
					for com in set(partition.values()):
						c+=1.
						print("COMMUNITY NUMBER " + str(com+1))
						list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
						count += print_graph(DG.subgraph(list_nodes), unique = True)
						nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,node_color = str((c / size)-1./(size*2)))

					return count



				pl = input("plot: ")

				if pl ==  "y" or pl == "yes":
					totcount+=print_community(partition, G, plot = True)
					nx.draw_networkx_edges(G, pos, alpha=0.5)
					plt.show()
				else:
					totcount+= print_community(partition, G)

				return totcount

	# for com in set(partition.values()) :
	# 	count = count + 1.
	# 	list_nodes = [nodes for nodes in partition.keys()
	# 								if partition[nodes] == com]
	# 	nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
	# 								node_color = str(count / size), cmap = "cool")
	# nx.draw_networkx_edges(G, pos, alpha=0.5)
	# plt.show()

if __name__ == "__main__":
	topic = "probability"
	from reader import reader
	from network import init
	data = reader(topic)
	DG = init(data)
	print("COUNT = "+ str(branch(data,DG)))
