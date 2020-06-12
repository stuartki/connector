import networkx as nx

import os
import sys
import operator
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

import nltk

from edit import edit
from Node import Node
from reader import reader
from network import mostPopularSuc, mostPopularPred, init, draw_all, cleanPred, most_degree_centrality, labeler
from load import txt_loader, pdf_loader, file_finder

# logic_dict = {
#   to: 
# }
def scaffold(data):
  for n in t_data:
    words = nltk.word_tokenize(n)
    print(n)
    print(nltk.pos_tag(words))
    input()

if __name__ == "__main__":
  path = "/Users/stuartki/Documents/pdfs/unifiedNLPArchitecture.pdf"
  if ".txt" in path:
    t_data = txt_loader(path)
  elif ".pdf" in path:
    t_data = pdf_loader(path)
  else:
    print("NO VALID FILE")
  scaffold(t_data)