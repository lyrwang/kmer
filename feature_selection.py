from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2
from sklearn.feature_selection import SelectPercentile, f_classif, RFE, RFECV
from sklearn.svm import SVC
from utils import flatten, make3D
import pandas as pd
import numpy as np

def variance_threshold(input_data, threshold=0.16, feature_names=None):
    """
    Removes all features from x_train and x_test whose variances is less
    than args[0] in x_train.
    """
    x_train = input_data[0]
    y_train = input_data[1]
    x_test = input_data[2]
    y_test = input_data[3]

    dims = len(x_train.shape)
    if dims == 3:
        x_train = flatten(x_train)
        x_test = flatten(x_test)
    feature_selector = VarianceThreshold(threshold=threshold)
    x_train = feature_selector.fit_transform(x_train)
    x_test = feature_selector.transform(x_test)
    if dims == 3:
        x_train = make3D(x_train)
        x_test = make3D(x_test)

    output_data = (x_train, y_train, x_test, y_test)

    if feature_names is not None:
        mask = feature_selector.get_support()
        selected_feature_names = feature_names[mask]
        output = (output_data, selected_feature_names)
    else:
        output = output_data
    return output


def remove_constant_features(input_data, feature_names=None):
    x_train = pd.DataFrame(input_data[0])
    x_train = x_train.loc[:, x_train.var() != 0.0]
    x_test = pd.DataFrame(input_data[2])
    x_test = x_test[list(x_train)]

    output_data=(np.asarray(x_train),input_data[1],np.asarray(x_test),input_data[3])

    if feature_names is not None:
        feature_names = feature_names[list(x_train)]
        output = (output_data, np.asarray(feature_names))
    else:
        output = output_data

    return output

def select_k_best(input_data, score_func=f_classif, k=500, feature_names=None):
    """
    Selects the k best features in x_train, removes all others from
    x_train and x_test. Selects the best features by using the score
    function score_func.
    """

    if score_func == f_classif:
        if feature_names is not None:
            input_data,feature_names = remove_constant_features(input_data, feature_names=feature_names)
        else:
            input_data = remove_constant_features(input_data)

    x_train = input_data[0]
    y_train = input_data[1]
    x_test = input_data[2]
    y_test = input_data[3]


    dims = len(x_train.shape)
    if dims == 3:
        x_train = flatten(x_train)
        x_test = flatten(x_test)
    feature_selector = SelectKBest(score_func=score_func, k=k)
    x_train = feature_selector.fit_transform(x_train, y_train)
    x_test = feature_selector.transform(x_test)
    if dims == 3:
        x_train = make3D(x_train)
        x_test = make3D(x_test)

    output_data = (x_train, y_train, x_test, y_test)
    if feature_names is not None:
        mask = feature_selector.get_support()
        selected_feature_names = feature_names[mask]
        output = (output_data, selected_feature_names)
    else:
        output = output_data
    return output


def select_percentile(input_data, score_func=f_classif, percentile=5, feature_names=None):
    """
    Selects the best args[1] percentile of features in x_train, removes
    the rest of the features from x_train and x_test. Selects the best
    features by using the score function args[0].
    """
    x_train = input_data[0]
    y_train = input_data[1]
    x_test = input_data[2]
    y_test = input_data[3]

    if score_func == f_classif:
        x_train, x_test = remove_constant_features(x_train, x_test)

    dims = len(x_train.shape)
    if dims == 3:
        x_train = flatten(x_train)
        x_test = flatten(x_test)
    feature_selector = SelectPercentile(score_func=score_func,
                                        percentile=percentile)
    x_train = feature_selector.fit_transform(x_train, y_train)
    x_test = feature_selector.transform(x_test)
    if dims == 3:
        x_train = make3D(x_train)
        x_test = make3D(x_test)

    output_data = (x_train, y_train, x_test, y_test)
    if feature_names is not None:
        mask = feature_selector.get_support()
        selected_feature_names = feature_names[mask]
        output = (output_data, selected_feature_names)
    else:
        output = output_data
    return output


def recursive_feature_elimination(input_data, estimator=SVC(kernel='linear'),
                                  n_features_to_select=None, step=0.1, feature_names=None):
    """
    Recursively eliminates features from x_train and x_test, see
    documentaion: http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html
    If providing args, it should be of the form:
    [estimator, n_features_to_select, step]
    """
    x_train = input_data[0]
    y_train = input_data[1]
    x_test = input_data[2]
    y_test = input_data[3]

    dims = len(x_train.shape)
    if dims == 3:
        x_train = flatten(x_train)
        x_test = flatten(x_test)
    feature_selector = RFE(estimator, n_features_to_select, step)
    x_train = feature_selector.fit_transform(x_train, y_train)
    x_test = feature_selector.transform(x_test)
    if dims == 3:
        x_train = make3D(x_train)
        x_test = make3D(x_test)

    output_data = (x_train, y_train, x_test, y_test)
    if feature_names is not None:
        mask = feature_selector.get_support()
        selected_feature_names = feature_names[mask]
        output = (output_data, selected_feature_names)
    else:
        output = output_data
    return output

def recursive_feature_elimination_cv(input_data, estimator=SVC(kernel='linear'),
                                     step=0.1, cv=3, feature_names=None):
    """
    Recursively elinates features from x_train and x_test using cross
    validation, see documentation: http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFECV.html
    If providing args, it should be of the form: [estimator, step, cv]
    """
    x_train = input_data[0]
    y_train = input_data[1]
    x_test = input_data[2]
    y_test = input_data[3]

    dims = len(x_train.shape)
    if dims == 3:
        x_train = flatten(x_train)
        x_test = flatten(x_test)
    feature_selector = RFECV(estimator, step, cv)
    x_train = feature_selector.fit_transform(x_train, y_train)
    x_test = feature_selector.transform(x_test)
    if dims == 3:
        x_train = make3D(x_train)
        x_test = make3D(x_test)

    output_data = (x_train, y_train, x_test, y_test)
    if feature_names is not None:
        mask = feature_selector.get_support()
        selected_feature_names = feature_names[mask]
        output = (output_data, selected_feature_names)
    else:
        output = output_data
    return output
