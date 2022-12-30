import pandas as pd
from sklearn.model_selection import train_test_split


def load_dataset(file_name):
    return pd.read_csv(file_name)


def transfer_str_to_numeric_vals(dataset):
    dt = dataset.copy()
    dt = dt.dropna(axis='index', how='any')
    dt.drop_duplicates(keep='first', inplace=True)
    for col in dt.columns:
        lables = dt[col].astype('category').cat.categories.tolist()
        replace__map_comp = {col: {k: v for k, v in zip(lables, list(range(0, len(lables) + 1)))}}
        dt.replace(replace__map_comp, inplace=True)
    return dt


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
