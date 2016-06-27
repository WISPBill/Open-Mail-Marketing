import fnmatch
import os
import csv
import shapely
from shapely.geometry import Polygon
import time
import json
import sys

data = json.loads(sys.argv[1])

mainpoly = []

for cordset in data:
	cordset[0] = float(cordset[0])
  	cordset[1] = float(cordset[1])
  	cordsset = tuple(cordset)
  	mainpoly.append(cordsset)
inputcov = tuple(mainpoly)

polygon = Polygon(inputcov)

matches = []
needfiles = []
for root, dirnames, filenames in os.walk('OpenAddressData/summary/us/'):
    for filename in fnmatch.filter(filenames, '*.csv'):
		matches.append(os.path.join(root, filename))
		for file in matches:
			with open(file, 'rb') as csvfile:
		  		 reader = csv.reader(csvfile, delimiter=',')
		  		 for row in reader:
						item = row[3]
						if (item != 'area'):
							poly = []
							item = item.replace("POLYGON", "")
							item = item.replace("((", "")
							item = item.replace("))", "")
							data = item.split(',')
							for cord in data:
								cord2 = cord.split()
  			 					cord2[0] = float(cord2[0])
  	  							cord2[1] = float(cord2[1])
  	  							cords = tuple(cord2)
  	  							poly.append(cords)
							poly2 = tuple(poly)
  	  						cov = Polygon(poly2)
  	  						if polygon.intersects(cov):
  	  							needfiles.append(file)
		  		 csvfile.flush()
		  		 csvfile.close()
needfiles = set(needfiles)
needfiles = list(needfiles)  

good = []
for file in needfiles:
	file = file.replace("-summary", "")
	file = file.replace("/summary/", "/Data/")
	with open(file, 'rb') as csvfile2:
		reader = csv.reader(csvfile2, delimiter=',')
		for row in reader:
			if(row[0] != 'LON'):
				point = shapely.geometry.Point(float(row[0]), float(row[1])) # longitude, latitude
				if polygon.contains(point):
					good.append(row)

print json.dumps(good)
