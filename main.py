
# install dpkt 
# to install basemap on windows I had to use anaconda as the whl file for windows did not work
# conda install proj4
# conda create --name TEST python=3.7
# conda activate TEST
import dpkt 
import os, sys
#Environment variable is needed to import Basemap
os.environ["PROJ_LIB"] = "C:\\Users\\standard\\Anaconda3\\pkgs\\proj4-5.2.0-hfa6e2cd_1001\\Library\\share"
from mpl_toolkits.basemap import Basemap
import socket
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt


file = open('botnet-capture-20110815-fast-flux.pcap', 'rb')

packet = dpkt.pcap.Reader(file)

addresses = {}
locations = {}

all_addresses = []
# all_sources = []
# all_destinations = []

# ts is the timestamp and buf contains everything else
for ts, buf in packet:
	eth = dpkt.ethernet.Ethernet(buf)
	if isinstance(eth.data, dpkt.ip.IP):
		ip = eth.data
		addresses[socket.inet_ntoa(ip.src)] = socket.inet_ntoa(ip.dst)
		
for src, dst in addresses.items():
	if src not in all_addresses:
		all_addresses.append(src)
	if dst not in all_addresses:
		all_addresses.append(dst)

def getInput():
	while(True):
		answer = input("|>")
		answer = answer.lower()
		if answer is None or "help" in answer:
			help()
		if "print" in answer:
			if "addresses" in answer:
				printAddresses()
			if "location" in answer:
				printLocations()
		if "draw" in answer:
			drawMap()
		if "exit" in answer:
			exit()
def help():
	print("TODO: add help")
	
def printAddresses():
	for src, dst in addresses.items():
		print(str(src) + " -> " + str(dst))

		
def getLocations():
	print("getting locations...")
	for x in all_addresses:
		url = 'http://www.geoip-db.com/json/{0}'.format(x)
		response = urlopen(url)
		data = json.load(response)
		locations[x] = data

def printLocations():
	getLocations()
	for x, y in locations.items():
		print(str(x) + ": " + str(y["country_name"]))

# should eventually make this a class and handle all the graphics with that
def drawMap():
	if locations:
		print("drawing map...")
		coordinates = []
		
		for ip, loc_data in locations.items():
			if loc_data["latitude"] != "Not found":
				coordinates.append([ip, loc_data["latitude"], loc_data["longitude"]])	
				
		fig = plt.figure(figsize=(10, 8), edgecolor='w')		
		map = Basemap(projection='mill', llcrnrlat = -90, llcrnrlon = -180, urcrnrlat = 90, urcrnrlon = 180, resolution='l')
		map.drawcoastlines()
		map.drawcountries(linewidth=2)
		map.bluemarble()
		for loc in coordinates:	
			ip, lat, lon = loc
			xpt, ypt = map(lon, lat)
			map.plot(xpt, ypt, 'co', markersize=8)
			for idx, val in enumerate(coordinates):
				if addresses[ip] in val:
					dst_ip, dst_lat, dst_lon = coordinates[idx]
					dst_x, dst_y = map(dst_lon, dst_lat)
					map.plot(dst_x, dst_y, 'co', markersize=8)
					xs = []
					ys = []
					xs.append(xpt)
					xs.append(dst_x)
					ys.append(ypt)
					ys.append(dst_y)
					map.plot(xs, ys, color='r', linewidth=3)

		plt.show()
	else:
		getLocations()
		drawMap()

getInput()
