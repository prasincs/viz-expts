#!/usr/bin/env python
from random import random

chromosomes = {}

def generate_histograms():
  with open("data/karyotype.txt") as karyotypes:
      for line in karyotypes.readlines():
        line = line.strip()
        if line[:4] == 'band':
          items = line.split(' ')
          if not chromosomes.has_key(items[1]):
            chromosomes[items[1]] = []
          chromosomes[items[1]].append((items[4], items[5],))
  print chromosomes 
  print "generating histograms"
  with open("data/histograms.txt", "w") as histograms:
    for k, v in chromosomes.items():
      for index, tup in enumerate(v):
        rand_num = 0
        while rand_num < 0.2:
          rand_num = round(random(),3)
        x, y = map(int, tup)
        if index < len(chromosomes[k])-1:
          y -=1
        histograms.write( " ".join([k, str(x), str(y), str(rand_num)]))
        histograms.write("\n")

   
if __name__ == "__main__":
  generate_histograms()
