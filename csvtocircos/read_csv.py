import csv
from string import strip
from Cheetah.Template import Template
reader = csv.reader(open('data.csv', 'rb'))

colors = ['red', 'green', 'blue']

dataDir = "data"
templatesDir = "templates"
chrs = {}
rowNames = []
fieldNames = []
for index, row in enumerate(reader):
  if index == 0:
    fieldNames = map(strip, row[1:])
    for field in fieldNames:
      chrs[field] = []
    continue
  rowNames.append(row[0])
  for i, field in enumerate(fieldNames):
    chrs[field].append(float(row[i+1]))


karyotypesFile = open(dataDir+"/karyotypes.txt", "w")
highlightsFile = open(dataDir+"/highlights.txt", "w")

# Generate Chromosomes
sums = {}
for k, v in chrs.items():
  sums[k] = sum(v)

total = sum([v for k,v in sums.items()])

# Create start and end values
indices = {}
n = 0
for f in fieldNames:
  v = sums[f]
  indices[f] = {'start': n, 'end'  : n+v}
  n+= v

for k in fieldNames:
  v = chrs[k] 
  karyotypesFile.write( "chr - {0} {0} {1} {2}\n".format(k, indices[k]['start'], indices[k]['end'] ))
  highlightsFile.write('{0} {1} {2} fill_color=green\n'.format(k, indices[k]['start'],indices[k]['end']))

highlightsFile.close()

# Make bands' start end values
def incsums(start,lst):
  l = []
  sum  = start
  for i in range(len(lst)):
    l.append(sum)
    if i < len(lst)-1:
      sum += lst[i]
  return l

ii = {}
for i, f in enumerate(fieldNames):
  #print f,indices[f]
  start = indices[f]['start']
  #print incsums(start, chrs[f]+[sums[f]])
  iSums = incsums (start, chrs[f]+ [sums[f]])
  print iSums
  ii[f] = {}
  for j in range(len(iSums)-1):
     ii[f][rowNames[j]] = {"start": iSums[j], "end": iSums[j+1]}

#Oh man, it's 6am and my variable names are getting crappier
#TODO fix that after sleep

for f in fieldNames:
  for i,r in enumerate(rowNames):
    karyotypesFile.write( "band {0} {1} {1} {2} {3} {4}\n".format(f,r,ii[f][r]['start'], ii[f][r]['end'], colors[i]))

karyotypesFile.close()

for i,r in enumerate(rowNames):
  segDupFilePath = "data/segdup{0}.txt".format(i)
  with open(segDupFilePath, "w") as f:
    for field in fieldNames:
      f.write("segdup{0} {1} {2} {3}\n".format(i, field, ii[field][r]['start'], ii[field][r]['end']))

with open(templatesDir+"/circos.conf.t","r") as f:
  definition = f.read()
  with open(dataDir+'/circos.conf','w') as g:
    items = []
    for i in range(len(rowNames)):
      items.append ({'id': i, 'color': colors[i]})
    g.write(Template(definition, searchList = [{'links': items}]))
