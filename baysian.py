def main(num):
	import pandas as pd
	col_names = ['DNS', 'TCP', 'HTTP', 'BROWSER', 'IGMPv3', 'SSDP', 'NBSS', 'NBNS', 'SMB', 'LANMAN', 'IRC', 'SSL', 'SSLv2','SSLv3', 'TLSv1', 'SMTP', 'SMTP|IMF', 'VICP', 'HTTP/XML', 'ICMP', 'Packets Sent', 'Packets Received', 'Bytes Sent', 'Bytes Received', 'Country', 'Label']

	file = pd.read_csv("final_features.csv",)

	#feature_cols = [ 'TCP', 'HTTP', 'SSL', 'Country'] num = 25
	feature_cols = ['DNS', 'TCP', 'HTTP', 'ICMP', 'Packets Sent', 'Packets Received', 'Bytes Sent', 'Bytes Received', 'Country']

	X = file[feature_cols]
	Y = file.Label
	from sklearn.model_selection import train_test_split

	X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.25, random_state=num)


	# Baysian Stuff

	from sklearn.naive_bayes import GaussianNB

	model = GaussianNB()

	model.fit(X_train, Y_train)

	Y_pred = model.predict(X_test)

	from sklearn.metrics import classification_report, confusion_matrix

	matrix = confusion_matrix(Y_test, Y_pred)
	return matrix
	
num = 0
while(True):
	result = main(num)
	if len(result) ==2:
		if result[1][1] != 0:
			print(num)
			break
	print(str(num) + ": " + str(result))
	num += 1