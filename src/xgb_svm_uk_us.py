#!/usr/bin/env python


import numpy as np
from xgboost import XGBClassifier
from keras.utils import np_utils, to_categorical
from sklearn.model_selection import StratifiedKFold, StratifiedShuffleSplit
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import matthews_corrcoef, classification_report, precision_recall_fscore_support
import collections
from sklearn.externals import joblib
import sys
from sklearn import preprocessing

from model_evaluators import *
from data_transformers import *

if __name__ == "__main__":
	#leave at 0 features for no feature selection
	num_feats = int(sys.argv[1])

	# can be SVM or XGB
	model_type = sys.argv[2]

	#print("Predicting for:", predict_for)
	#print("on {} features".format(num_feats))

	kmer_matrix   = np.load('data/uk_us_unfiltered/kmer_matrix.npy')
	class_array   = np.load('data/uk_us_unfiltered/kmer_rows_Class.npy')
	dataset_array = np.load('data/uk_us_unfiltered/kmer_rows_Dataset.npy')

	train_mask = np.asarray[i =='Train' for i in dataset_array]
	test_mask  = np.asarray[i =='Test'  for i in dataset_array]


	le = preprocessing.LabelEncoder()
	class_array = le.fit_transform(class_array)
	num_classes = len(le.classes_)

	x_train = kmer_matrix[train_mask] #UK
	y_train = class_array[train_mask] #UK
	x_test  = kmer_matrix[test_mask]  #US
	y_test  = class_array[test_mask]  #US

	num_threads = 64

	cvscores = []
	window_scores = []
	mcc_scores = []
	report_scores = []
	split_counter = 0

	if(num_feats!=0):
		sk_obj = SelectKBest(f_classif, k=num_feats)
		x_train = sk_obj.fit_transform(x_train, y_train)
		x_test  = sk_obj.transform(x_test)


	model = XGBClassifier(learning_rate=1, n_estimators=10, objective='multi:softmax', silent=True, nthread=num_threads)
	model.fit(x_train,y_train)

	results = xgb_tester(model, x_test, y_test, 0)
	OBOResults = xgb_tester(model, x_test, y_test, 1)

	window_scores.append(OBOResults[0])
	mcc_scores.append(results[1])

	labels = np.arange(0,num_classes)
	report = precision_recall_fscore_support(results[3], results[2], average=None, labels=labels)
	report_scores.append(report)
	cvscores.append(results[0])

	print("Predicting for:", predict_for)
	print("on {} features".format(num_feats))
	print("Avg base acc:   %.2f%%   (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
	print("Avg window acc: %.2f%%   (+/- %.2f%%)" % (np.mean(window_scores), np.std(window_scores)))
	print("Avg mcc:        %f (+/- %f)" % (np.mean(mcc_scores), np.std(mcc_scores)))

	np.set_printoptions(suppress=True)
	avg_reports = np.mean(report_scores,axis=0)
	avg_reports = np.transpose(avg_reports)
	avg_reports = np.around(avg_reports, decimals=2)
	print(avg_reports)
	print(le.classes_)
