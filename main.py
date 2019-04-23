

# install dpkt 
# to install basemap on windows I had to use anaconda as the whl file for windows did not work
# conda install proj4
# conda create --name TEST python=3.7
# conda activate TEST
import dpkt 
import os, sys
#Environment variable is needed to import Basemap
os.environ["PROJ_LIB"] = "C:\\Users\\standard\\Anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\\share"
from mpl_toolkits.basemap import Basemap
import socket
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

file = open('botnet-capture-20110815-fast-flux.pcap', 'rb')

packet = dpkt.pcap.Reader(file)

addresses = []
locations = {}
arrow_size = 250000
all_addresses = []
# all_sources = []
# all_destinations = []
	

# ts is the timestamp and buf contains everything else
for ts, buf in packet:
	eth = dpkt.ethernet.Ethernet(buf)
	if isinstance(eth.data, dpkt.ip.IP):
		ip = eth.data
		if [socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst)] not in addresses:
			addresses.append([socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst)])
		
for items in addresses:
	if str(items[0]) not in all_addresses:
		all_addresses.append(str(items[0]))
	if str(items[1]) not in all_addresses:
		all_addresses.append(str(items[1]))

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
		if "info" in answer:
			info()
		if "get countries" in answer:
			getCountries()
def help():
	print("TODO: add help")
	
def printAddresses():
	for items in addresses:
		print(str(items[0]) + " -> " + str(items[1]))

		
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
		ax = plt.axes()
		map = Basemap(projection='mill', llcrnrlat = -90, llcrnrlon = -180, urcrnrlat = 90, urcrnrlon = 180, resolution='l')
		map.drawcoastlines()
		map.drawcountries(linewidth=2)
		map.bluemarble()
		print("drawing markers...")
		
		for cord in coordinates:
			ip, lat, lon = cord
			if lon is None or lat is None:
				continue
			else:
				xpt, ypt = map(lon, lat)
				map.plot(xpt, ypt, 'ro', markersize=8)
				for idx, loc_entry in enumerate(coordinates):
					for items in addresses:
						if items[0] == ip and items[1] == loc_entry[0]:
							dst_ip, dst_lat, dst_lon = coordinates[idx]
							if dst_lat is not None:
								dst_x, dst_y = map(dst_lon, dst_lat)
								map.plot(dst_x, dst_y, 'ro', markersize=8, zorder=20)
								if (math.sqrt(((dst_x -xpt)**2) +  ((dst_y -ypt)**2))) != 0:
									#ax.arrow(xpt, ypt, (dst_x - xpt), (dst_y - ypt), color='r', lw=3, head_width=50000, head_length=50000 * 1.5)
									ax.arrow(xpt, ypt, (dst_x - xpt), (dst_y - ypt), width=arrow_size, length_includes_head=True, facecolor='c', edgecolor='k', zorder=15)
									print(str(math.sqrt(((dst_x -xpt)**2) +  ((dst_y -ypt)**2))))
									

		plt.show()
	else:
		getLocations()
		drawMap()

def info():
	answer = input("enter IP address:")
	srcs = []
	dsts = []
	if len(answer) == 0:
		for items in addresses:
			print(str(items[0]) + " -> " + str(items[1]))
	else:
		print("IP addresses that send data to " + answer)
		for val in addresses:
			if val[1] == answer:
				srcs.append(val[1])
				print(val[0])
		
		print("IP addresses that receive data from " + answer)
		for val in addresses:
			if val[0] == answer:
				dsts.append(val[0])
				print(val[0])
		print("Countries that accessed " + answer)
		src_countries = []
		for ips, loc_data in locations.items():
			if ips in srcs:
				if ips not in src_countries:
					src_countries.append(loc_data["country_name"])
					
		for countries in src_countries:
			print(countries)

def getCountries():
	file = open("countries.txt", 'a')
	for x, y in locations.items():
		file.write(str(x) + ": " + str(y["country_name"]) + "\n")
getInput()
