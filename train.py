
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split


import pickle

from utils import build_features



def metric(ytest,y_predicted):
	#precision =  # tp/  tp + fp
	#recall =  # tp /tp + fn

	tp = sum([ ytest[i]==y_predicted[i] for i in range(len(ytest))])

	fp=0
	fn = 0

	for i in range(len(ytest)):
	    if ytest[i]!=y_predicted[i]:
	        if ytest[i]:
	            fn=fn+1
	        else:
	            fn = fn + 1

	print("tp, fp, fn and len of test set is respectively", tp, fp, fn, len(ytest))

	precison = tp/(fp + tp)
	recall = tp/(tp +fn)

	print("precision is : ", precison)
	print("recall is : ", recall)


def main():

	with open("training_data.csv",'r') as f:
	    data = f.readlines()


	X = [i.strip()[:-2] for i in data[1:]]
	X = [build_features(i) for i in X]
	Y = [i.strip()[-1] for i in data[1:]]

	print(" total data availabel is ", len(X))

	Xtrain, Xtest, ytrain, ytest = train_test_split(X, Y)

	clf = DecisionTreeClassifier(max_depth=3)
	y_score = clf.fit(Xtrain, ytrain)

	print("model training succesful.......... ",)

	y_predicted = clf.predict(Xtest)

	metric(ytest, y_predicted)

	with open("model.pickle", 'wb') as pickle_file:
		pickle.dump(clf, pickle_file)

	print("model saved succesfully.............")


if __name__ == '__main__':
	main()