import os  # for testing use only

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# --------cross-validation
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
# -------- classification
import sklearn
from sklearn import neighbors, tree, ensemble, naive_bayes, svm
# *** KNN
from sklearn.neighbors import KNeighborsClassifier
# *** Decision Tree; Random Forest
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# *** Naive Bayes
from sklearn.naive_bayes import GaussianNB
# *** SVM classifier
from sklearn.svm import SVC
# --------  metrics:
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import make_scorer


def load_dataset(file_name):
    return pd.read_csv(file_name)


def transfer_str_to_numeric_vals(dataset):
    dt_copy = dataset.copy()
    dt_copy = dataset.dropna(axis='index', how='any')
    dt_copy = dt_copy.drop_duplicates(keep='first')
    for i in dt_copy.columns:
        i_label = dt_copy[i].astype('category').cat.categories.tolist()
        instead = {i: {p: t for p, t in zip(i_label, list(range(0, len(i_label) + 1)))}}
        dt_copy = dt_copy.replace(instead)
    return dt_copy


def split_to_train_and_test(dataset, label_column, test_ratio, rand_state):
    j = 0
    X = dataset.copy()
    y = dataset.copy()
    for data in X.columns:
        if data == label_column:
            y = X.iloc[:, j]
            X.drop(X.columns[j], axis=1, inplace=True)
        else:
            j += 1
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=rand_state)
    return X_train, X_test, y_train, y_test


def find_best_model(X_train, y_train, max_depth_val, min_samples_split_val):
    recall_score = make_scorer(metrics.recall_score)
    print(recall_score)
    clf1 = DecisionTreeClassifier(max_depth=max_depth_val, min_samples_split=min_samples_split_val)
    clf1_cross = cross_val_score(clf1, X_train, y_train, scoring=recall_score, cv=5)
    clf1_score = clf1_cross.mean()
    clf2 = GaussianNB()
    clf2_cross = cross_val_score(clf2, X_train, y_train, scoring=recall_score, cv=5)
    clf2_score = clf2_cross.mean()
    clf3 = SVC()
    clf3_cross = cross_val_score(clf3, X_train, y_train, scoring=recall_score, cv=5)
    clf3__score = clf3_cross.mean()
    best_recall_val = max(clf1_score, clf2_score, clf3__score)
    if best_recall_val == clf1_score:
        best_clf = DecisionTreeClassifier()
    elif best_recall_val == clf2_score:
        best_clf = clf2
    else:
        best_clf = clf3
    return best_clf, best_recall_val
