import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.layers.pooling import AveragePooling1D
from keras.layers.convolutional import Conv1D
from sklearn import svm
from utils import flatten, make3D, convert_to_numerical_classes
from keras.utils import to_categorical
from sklearn.ensemble import RandomForestClassifier


def neural_network_validation(input_data):
    """
    Constructs, compiles, trains, and tests a neural network.
    Returns the accuracy of the model.
    """
    input_data, le = convert_to_numerical_classes(input_data)

    x_train = input_data[0]
    y_train = input_data[1]
    x_test = input_data[2]
    y_test = input_data[3]

    train_classes = np.unique(np.asarray(y_train))
    test_classes = np.unique(np.asarray(y_test))
    classes = np.unique(np.hstack((train_classes, test_classes)))
    num_classes = classes.shape[0]

    y_train = to_categorical(y_train, num_classes=num_classes)
    y_test = to_categorical(y_test, num_classes=num_classes)

    if len(x_train.shape) == 2:
        x_train = make3D(x_train)
        x_test = make3D(x_test)
    model = Sequential()
    model.add(Conv1D(filters=10,
                     kernel_size=3,
                     activation='relu',
                     padding='same',
                     input_shape = (x_train.shape[1], 1)))
    model.add(Flatten())
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer = 'adam',
                  loss = 'binary_crossentropy',
                  metrics = ['accuracy'])
    model.fit(x_train, y_train, epochs=50, batch_size=10, verbose=0)
    evaluation = model.evaluate(x_test, y_test, batch_size=1, verbose=0)
    return evaluation[1]


def neural_network(input_data, binarize=True):
    """
    Constructs, compiles, trains and makes predictions with a neural network.
    Returns the predicted values for "predict". If args[0] is true the
    predictions will be 0's and 1's if not the predictions will be floats
    between 0.0 and 1.0 with values closer to 0.0 and 1.0 indicating a higher
    probability of the prediction being correct.
    If args is not provided, default values will be used.
    """
    input_data = input_data[:-1]
    input_data, le = convert_to_numerical_classes(input_data)

    print le.inverse_transform([0,1,2,3,4])

    x_train = input_data[0]
    y_train = input_data[1]
    predict = input_data[2]

    train_classes = np.unique(np.asarray(y_train))
    num_classes = len(list(train_classes))

    y_train = to_categorical(y_train)

    if len(x_train.shape) == 2:
        x_train = make3D(x_train)
        predict = make3D(predict)
    model = Sequential()
    model.add(Conv1D(filters=10,
                     kernel_size=3,
                     activation='relu',
                     input_shape = (x_train.shape[1], 1)))
    model.add(Flatten())
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='adam',
                  loss = 'binary_crossentropy',
                  metrics = ['accuracy'])
    model.fit(x_train, y_train, epochs=50, batch_size=10, verbose=0)
    prediction = model.predict(predict)
    if binarize:
        prediction = np.where(prediction > 0.5, 1, 0)
    return prediction


def support_vector_machine_validation(input_data, kernel='linear', C=1):
    """
    Fits, trains, and test a support vector machine.
    Returns the accuracy of the model.
    """
    x_train = input_data[0]
    y_train = input_data[1]
    x_test = input_data[2]
    y_test = input_data[3]
    if len(x_train.shape) == 3:
        x_train = flatten(x_train)
        x_test = flatten(x_test)
    model = svm.SVC(kernel=kernel, C=C)
    model.fit(x_train, y_train)
    return model.score(x_test, y_test)


def support_vector_machine(input_data, kernel='linear', C=1):
    """
    Fits, trains, and makes predictions with a support vector machine.
    Returns the predicted values for "predict"
    """
    x_train = input_data[0]
    y_train = input_data[1]
    predict = input_data[2]

    if len(x_train.shape) == 3:
        x_train = flatten(x_train)
        x_test = flatten(x_test)
    model = svm.SVC(kernel=kernel, C=C)
    model.fit(x_train, y_train)
    return model.predict(predict)

def random_forest_validation(input_data,n_estimators=5,criterion='gini',
                             max_features=None,max_depth=None,
                             min_samples_split=5,min_samples_leaf=1,
                             min_weight_fraction_leaf=0.1,
                             max_leaf_nodes=10,min_impurity_decrease=0,
                             bootstrap=True, n_jobs=-1):
    x_train = input_data[0]
    y_train = input_data[1]
    x_test = input_data[2]
    y_test = input_data[3]
    if len(x_train.shape) == 3:
        x_train = flatten(x_train)
        x_test = flatten(x_test)
    kwargs = {'n_estimators': n_estimators, 'criterion': criterion,
              'max_features': max_features, 'max_depth': max_depth,
              'min_samples_split': min_samples_split,
              'min_samples_leaf':min_samples_leaf,
              'min_weight_fraction_leaf': min_weight_fraction_leaf,
              'max_leaf_nodes':max_leaf_nodes,
              'min_impurity_decrease': min_impurity_decrease,
              'bootstrap': bootstrap, 'n_jobs': n_jobs}
    model = RandomForestClassifier(**kwargs)
    model.fit(x_train, y_train)
    return model.score(x_test, y_test)
