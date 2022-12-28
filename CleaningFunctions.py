import numpy as np


def remove_duplicative(df, col_name=None):
    if col_name is None:
        return df.drop_duplicates()
    return df.drop_duplicates(subset=[col_name])


def remove_corrupt_rows(df, num_max_missing_cols):
    return df.dropna(thresh=df.shape[1] - num_max_missing_cols)


def outlier_detection_zscore_dist(df):
    df_copy = df.copy()
    numeric_num_cols = df_copy._get_numeric_data().columns
    for col in numeric_num_cols:
        if df_copy[col].dtypes != object:
            z_score = (df[col] - df[col].mean()) / df[col].std()
            df_copy.loc[abs(z_score) > 3, [col]] = np.nan
    return df_copy
