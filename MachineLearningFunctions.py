import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.svm import SVC
import numpy as np

"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : load_dataset.
Describe function : 
    This function creates and returns data set csv file with a given string - file name.
Origin of code : 
    From our home assignments.
"""


def load_dataset(file_name):
    return pd.read_csv(file_name)


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : transfer_str_to_numeric_vals.
Describe function : 
    * Remove any rows with one or more missing value. 
    * For any duplicate rows, keep only the first one. 
    * Transfer dataset's values to numeric ones.
Origin of code : 
    From our home assignments.
"""


def transfer_str_to_numeric_vals(dataset):
    dt = dataset.copy()
    dt = dt.dropna(axis="index", how="any")
    dt.drop_duplicates(keep="first", inplace=True)
    for col in dt.columns:
        value = dt[col].astype("category").cat.categories.tolist()
        replace__map_comp = {col: {k: v for k, v in zip(value, list(range(0, len(value) + 1)))}}
        dt.replace(replace__map_comp, inplace=True)
    return dt


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : split_to_train_and_test.
Describe function : 
    * Split the given dataset into 'X' (feature vectors - dataframe) and 'y' (corresponding labels - series), 
    determined by the given 'label_column' column.
    * Split X and y into 'X_train', 'X_test', and corresponding 'y_train' and 'y_test' series.
Origin of code : 
    From our home assignments.
"""


def split_to_train_and_test(dataset, label_column, test_ratio, rand_state):
    i = 0
    for col in dataset.columns:
        if col == label_column:
            y = dataset.iloc[:, i]
            dataset.drop(dataset.columns[i], axis=1, inplace=True)
            continue
        i += 1
    X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=test_ratio, random_state=rand_state)
    return X_train, X_test, y_train, y_test


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : get_data_ready.
Describe function : 
    This function drops columns that has we don't wand to appear in the next stage,
     and calls transfer_str_to_numeric_vals. 
     It returns data frame from csv file name given.
Origin of code : 
    We wrote this code for the project.
"""


def get_data_ready(file_name):
    raw_dataset = load_dataset(file_name)
    raw_dataset.drop(
        columns=["Hotel name", "Hotel url", "Rating regarding other hotels in the same city"],
        inplace=True)
    return raw_dataset


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : check_eda_method.
Describe function : 
    This function checks 4 eda methods and calls another function that visualize the results.
Origin of code : 
    From our own course lecture, and we wrote this code for the project.
"""


def check_eda_method(X_train, X_test, y_train, y_test):
    clf1 = DecisionTreeClassifier()
    clf2 = RandomForestClassifier()
    clf3 = GaussianNB()
    clf4 = KNeighborsClassifier()
    clf5 = DecisionTreeClassifier()
    colors_arr = ["b", "g", "r", "c", "m", "y", "k"]
    idx_colors = 0
    alg_names = ["decision_tree", "random_forest", "naive_bayes", "knn", "decision_tree"]
    alg_number = len(alg_names)
    for idx, clf in enumerate([clf1, clf2, clf3, clf4, clf5]):
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_pred_train = clf.predict(X_train)
        print(alg_names[idx])
        print(f"accurate on train is {metrics.accuracy_score(y_true=y_train, y_pred=y_pred_train)}")
        print(f"accurate on test is {metrics.accuracy_score(y_true=y_test, y_pred=y_pred)}")
        print("Confusion matrix is:")
        print(metrics.confusion_matrix(y_test, y_pred))
        eda_result_visualization(y_test.values.tolist(), y_pred, alg_names[idx], colors_arr[idx_colors],
                                 colors_arr[(idx_colors + 1)])
        idx_colors = (idx_colors + 2) % alg_number
        print("------------------------------------------------------------------")


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : eda_result_visualization.
Describe function : 
    This function gets results from check_eda_method visualize the results and print it to png file.
Origin of code : 
    We wrote this code for the project.
"""


def eda_result_visualization(y_test_origin, y_test_predict, alg_name, color1, color2):
    width = 0.20
    y_test_origin_len = len(y_test_origin)
    y_test_predict_len = len(y_test_predict)
    jump = int(y_test_origin_len / 14)
    bar1 = plt.bar(np.arange(len(y_test_origin[0:y_test_origin_len:jump])), y_test_origin[0:y_test_origin_len:jump],
                   width, color=color1)
    bar2 = plt.bar(np.arange(len(y_test_predict[0:y_test_predict_len:jump])) + width,
                   y_test_predict[0:y_test_predict_len:jump], width, color=color2)
    plt.legend((bar1, bar2), ("Original", "Prediction test"))
    plt.title("Tripadvisor rating EDA " + alg_name)
    plt.xlabel("Hotel examples")
    plt.ylabel("Tripadvisor rating")
    plt.savefig("EDA results graph " + alg_name + ".png")
    plt.close()
