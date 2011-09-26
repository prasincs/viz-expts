#!/usr/bin/env python
import csv
from string import strip
from Cheetah.Template import Template
import os,subprocess
from histograms import *
dataDir = 'data'
templatesDir = 'templates'
htmlDir = 'html'
colors = ['red', 'green', 'blue', 'grey', 'black', 'orange']

CIRCOS_EXEC = "circos"


class CsvToCircos(object):
 
  def __init__(self, csv_file = 'data.csv'):
    self.csv_file = csv_file
    self.chrs = {}
    self.rowNames = []
    self.fieldNames = []
    self.bandsIndex = {}
    self.total = 0
  
  def writeFiles(self):
    self.openFile()
    self.writeKaryotypesFile()
    generate_histograms()
    self.writeConfigFiles()

  def writeConfigFiles(self, rows = None):
    if (rows == None):
      rows = self.rowNames
    with open(dataDir+'/circos.conf','w') as f:
       items = []
       rr = [self.rowNames.index(i) for i in rows]
       for i in rr:
          items.append ({'id': i, 'color': colors[i]})
       units = self.total/(len(self.rowNames)*len(self.fieldNames)*10)
       if units < 1:
         units =1
       f.write(Template(file=templatesDir+"/circos.conf.tmpl", \
           searchList = [{'units': units, 'links': items}]).respond())

  def runCircos(self,outputFileName="circos.png"):
    print "running circos"
    savedPath = os.getcwd()
    os.chdir(dataDir)
    p = subprocess.Popen([CIRCOS_EXEC, "-conf", "circos.conf", "-outputfile", outputFileName], stdout=subprocess.PIPE)
    os.chdir(savedPath)
    return p


  def openFile(self):
    reader = csv.reader(open(self.csv_file, 'rb'))
    self.chrs = {}
    self.rowNames = []
    self.fieldNames = []
    for index, row in enumerate(reader):
      if index == 0:
        self.fieldNames = map(strip, row[1:])
        for field in self.fieldNames:
          self.chrs[field] = []
        continue
      self.rowNames.append(row[0])
      for i, field in enumerate(self.fieldNames):
        self.chrs[field].append(int(row[i+1]))

  def writeKaryotypesFile (self):
    karyotypesFile = open(dataDir+"/karyotype.txt", "w")
    highlightsFile = open(dataDir+"/highlights.txt", "w")

    # Generate Chromosomes
    sums = {}
    for k, v in self.chrs.items():
      sums[k] = sum(v)

    self.total = sum([v for k,v in sums.items()])

    # Create start and end values
    indices = {}
    n = 0
    for i, f in enumerate(self.fieldNames):
      v = sums[f] + len(self.rowNames)-1
      if i > 0:
        n +=1
      indices[f] = {'start': n, 'end'  : n+v}
      n+= v

    print indices

    for k in self.fieldNames:
      karyotypesFile.write( "chr - {0} {0} {1} {2}\n".format(k, indices[k]['start'], indices[k]['end'] ))
      highlightsFile.write('{0} {1} {2} fill_color=green\n'.format(k, indices[k]['start'],indices[k]['end']))

    highlightsFile.close()

    # Make bands' start end values
    self.bandsIndex = {}
    for i, f in enumerate(self.fieldNames):
      start = indices[f]['start']
      n = start
      self.bandsIndex[f] = {}
      for i, c in enumerate(self.chrs[f]):
        v = c 
        if i > 0:
          n+=1
        self.bandsIndex[f][self.rowNames[i]] = {'start': n, 'end': n+v}
        n += v


    for f in self.fieldNames:
      for i,r in enumerate(self.rowNames):
        karyotypesFile.write( "band {0} {1} {1} {2} {3} {4}\n".format(f,r,self.bandsIndex[f][r]['start'], self.bandsIndex[f][r]['end'], colors[i]))

    karyotypesFile.close()
  
    # Writing Link files
    for i,r in enumerate(self.rowNames):
      segDupFilePath = "data/segdup{0}.txt".format(i)
      with open(segDupFilePath, "w") as f:
        for field in self.fieldNames:
          f.write("segdup{0} {1} {2} {3}\n".format(i, field, self.bandsIndex[field][r]['start'], self.bandsIndex[field][r]['end']))
        field = self.fieldNames[0]
        f.write("segdup{0} {1} {2} {3}\n".format(i, field, self.bandsIndex[field][r]['start'], self.bandsIndex[field][r]['end']))



if __name__ == "__main__":
  csvToCircos = CsvToCircos('data.csv')
  csvToCircos.writeFiles()
  process = csvToCircos.runCircos()
  process.poll()
  for line in process.communicate():
    if line != None:
      print line

