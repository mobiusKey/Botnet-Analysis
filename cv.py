
import csv

# ip : [ ports, # of packets sent, ,# of packets received, bytes sent, bytes received, then country and malicous ]
data = {}

def checksrc(row):
	number, time, source, destination, protocol, length, info = row
	for key in data:
		if source == key:
			return True


	data.update({source: [protocol, 1, 0, int(length), 0]})
	
def checkdst(row):
	number, time, source, destination, protocol, length, info = row
	for key in data:
		if key == destination:
			return True
	data.update({destination: [protocol, 0, 1, 0, int(length)]})
	
with open("botnet.csv", "r") as file:
	reader = csv.reader(file, delimiter=",")
	for row in reader:
		number, time, source, destination, protocol, length, info = row

		if checksrc(row):
			ports, psent, prec, bsent, brec = data[source]
			if protocol not in ports:
				ports += " " + protocol
			psent += 1
			bsent += int(length)
			data[source] = [ports, psent, prec, bsent, brec]
		
		if checkdst(row):
			ports, psent, prec, bsent, brec = data[destination]
			prec += 1
			brec += int(length)
			data[destination] = [ports, psent, prec, bsent, brec]

		#print(number)

			

for ip, value in data.items():
	ports, psent, prec, bsent, brec = value
	print("{}: ports -> {} packets sent -> {} packets rec -> {} bytes sent -> {} bytes rec ->{}".format(ip,ports, psent, prec, bsent, brec))
				