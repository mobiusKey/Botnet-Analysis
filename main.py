import dpkt 
import os, sys
import socket
from urllib.request import urlopen
import json

file = open('botnet-capture-20110815-fast-flux.pcap', 'rb')

packet = dpkt.pcap.Reader(file)

addresses = {}
locations = {}

# ts is the timestamp and buf contains everything else
for ts, buf in packet:
	eth = dpkt.ethernet.Ethernet(buf)
	if isinstance(eth.data, dpkt.ip.IP):
		ip = eth.data
		addresses[socket.inet_ntoa(ip.src)] = socket.inet_ntoa(ip.dst)
		
for x, y in addresses.items():
	print(str(x) + " -> " + str(y))
		

for x in addresses:
	url = 'http://www.geoip-db.com/json/{0}'.format(x)
	response = urlopen(url)
	data = json.load(response)
	addresses[x] = data
	
for x, y in addresses.items():
	print(str(x) + ": " + str(y["country_name"]))