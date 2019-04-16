
import csv

# ip : [ ports, # of packets sent, ,# of packets received, bytes sent, bytes received, then country and malicous ]
data = {}

def checksrc(row):
	number, time, source, destination, protocol, length, info = row
	for key in data:
		if source == key:
			return True


	#data.update({source: [protocol, 1, 0, int(length), 0]})
	data.update({source: [{'DNS':0, 'TCP':0, 'HTTP':0, 'BROWSER':0, 'IGMPv3':0, 'SSDP':0, 'NBSS':0, 'NBNS':0, 'SMB':0, 'LANMAN':0, 'IRC':0, 'SSL':0, 'SSLv2':0,'SSLv3':0, 'TLSv1':0, 'SMTP':0, 'SMTP|IMF':0, 'VICP':0, 'HTTP/XML':0, 'ICMP':0}, 1, 0, int(length), 0]})
	data[source][0][protocol] = int(length)
def checkdst(row):
	number, time, source, destination, protocol, length, info = row
	for key in data:
		if key == destination:
			return True
	data.update({destination: [{'DNS':0, 'TCP':0, 'HTTP':0, 'BROWSER':0, 'IGMPv3':0, 'SSDP':0, 'NBSS':0, 'NBNS':0, 'SMB':0, 'LANMAN':0, 'IRC':0, 'SSL':0, 'SSLv2':0,'SSLv3':0, 'TLSv1':0, 'SMTP':0, 'SMTP|IMF':0, 'VICP':0, 'HTTP/XML':0, 'ICMP':0}, 0, 1, 0, int(length)]})
	data[destination][0][protocol] = int(length)
with open("botnet.csv", "r") as file:
	reader = csv.reader(file, delimiter=",")
	for row in reader:
		number, time, source, destination, protocol, length, info = row

		if checksrc(row):
			ports, psent, prec, bsent, brec = data[source]
			
			psent += 1
			bsent += int(length)
			ports[protocol] = ports[protocol] + int(length)
			data[source] = [ports, psent, prec, bsent, brec]
			
		if checkdst(row):
			ports, psent, prec, bsent, brec = data[destination]
			prec += 1
			brec += int(length)
			ports[protocol] = ports[protocol] + int(length)
			data[destination] = [ports, psent, prec, bsent, brec]

		#print(number)
		
file = open("countries.txt", 'r')
for line in file:
	ip, country = line.split(": ")
	country, _ = country.split("\n")
	for key in data:
		if key == ip:
			print(data[key])
			print(country)
			print(data[key].append(country))
for key in data:
	print(data[key])
			
file.close()
countries = {"Not found": 0, "None":0 }
num_countries = 1
with open('features.csv', mode='w') as feature_file:
	data_writer = csv.writer(feature_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	for ip, value in data.items():
		if len(value) ==6:
			ports, psent, prec, bsent, brec, country= value
			if country not in countries:
				countries[country] = num_countries
				num_countries += 1
			data_writer.writerow([ip, ports['DNS'], ports['TCP'], ports['HTTP'], ports['BROWSER'], ports['IGMPv3'], ports['SSDP'], ports['NBSS'], ports['NBNS'], ports['SMB'], ports['LANMAN'], ports['IRC'], ports['SSL'], ports['SSLv2'], ports['SSLv3'], ports['TLSv1'], ports['SMTP'], ports['SMTP|IMF'], ports['VICP'], ports['HTTP/XML'], ports['ICMP'], psent, prec, bsent, brec, countries[country]])
			
			print([ip, ports, psent, prec, bsent, brec, countries[country], country])
			
					
print(countries)

				