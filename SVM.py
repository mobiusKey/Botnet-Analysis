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

	from sklearn.svm import SVC

	model = SVC(kernel='linear')

	model.fit(X_train, Y_train)

	Y_pred = model.predict(X_test)

	from sklearn.metrics import classification_report, confusion_matrix

	matrix = confusion_matrix(Y_test, Y_pred)
	print(matrix)
	print(classification_report(Y_test, Y_pred))
	
	from sklearn import metrics
	print("Accuracy:", metrics.accuracy_score(Y_test, Y_pred))
	print("Precision:", metrics.precision_score(Y_test, Y_pred))
	print("Recall:", metrics.recall_score(Y_test, Y_pred))
	
	import numpy as np
	import matplotlib.pyplot as plt
	import seaborn as sns
	class_names=[0,1]
	fig, ax = plt.subplots()
	tick_marks = np.arange(len(class_names))
	plt.xticks(tick_marks, class_names)
	plt.yticks(tick_marks, class_names)
	
	cnf_matrix = confusion_matrix(Y_test, Y_pred)
	sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
	plt.tight_layout()
	plt.title('Confusion matrix', y=1.1)
	plt.ylabel('Actual label')
	plt.xlabel('Predicted label')
	plt.text(0.5,257.44,'Predicted label')
	plt.show()

num = 1323
result = main(num)
