import numpy as np

"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : remove_duplicative.
Describe function : 
    This function remove duplicate rows from data frame.
Origin of code : 
    From our home assignments.
"""


def remove_duplicative(df, col_name=None):
    if col_name is None:
        return df.drop_duplicates()
    return df.drop_duplicates(subset=[col_name])


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : remove_corrupt_rows.
Describe function : 
    This function removes lines from dataframe that has at least one missing parameter.
Origin of code : 
    From our home assignments.
"""


def remove_corrupt_rows(df):
    df.dropna(inplace=True)


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : outlier_detection_zscore_dist.
Describe function : 
    This function removes lines that it's data has numeric parameters and it's values are outliers.
Origin of code : 
    From our home assignments.
"""


def outlier_detection_zscore_dist(df):
    df_copy = df.copy()
    numeric_num_cols = df_copy._get_numeric_data().columns
    for col in numeric_num_cols:
        if df_copy[col].dtypes != object:
            z_score = (df[col] - df[col].mean()) / df[col].std()
            df_copy.loc[abs(z_score) > 3, [col]] = np.nan
    return df_copy
