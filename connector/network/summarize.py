import networkx as nx
import os
import sys
from Node import Node
from reader import reader
from edit import edit
import matplotlib.pyplot as plt
import operator
from collections import Counter
import pandas as pd

from network import mostPopularSuc, mostPopularPred, init, draw_all, cleanPred, most_degree_centrality, labeler

def summarize_old(data, DG):
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

def summarize(data, DG):
  leaves = [n for n,d in DG.out_degree() if d == 0]
  roots = [n for n,d in DG.in_degree() if d == 0]

if __name__ == "__main__":
	topic = "probability"
	from reader import reader
	from network import init
	data = reader(topic)
	DG = init(data)