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
		

def getInput():
	while(True):
		answer = input("|>")
		answer = answer.lower()
		if answer is None or "help in answer":
			help()
		if "print" in answer:
			if "addresses" in answer:
				printAddresses()
			if "location" in answer:
				printLocations()
				
def help():
	print("TODO: add help")
	
def printAddresses():
	for src, dst in addresses.items():
		print(str(src) + " -> " + str(dst))
		
def getLocations():
	print("getting locations...")
	for x in addresses:
		url = 'http://www.geoip-db.com/json/{0}'.format(x)
		response = urlopen(url)
		data = json.load(response)
		locations[x] = data

def printLocations():
	getLocations()
	for x, y in locations.items():
		print(str(x) + ": " + str(y["country_name"]))

getInput()
