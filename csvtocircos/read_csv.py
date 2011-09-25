import csv
reader = csv.reader(open('data.csv', 'rb'))

for row in reader:
  print ','.join(row)
