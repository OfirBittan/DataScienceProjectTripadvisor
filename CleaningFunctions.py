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
    From our home assignments..
"""


def remove_corrupt_rows(df):
    df.dropna(axis=0, inplace=True)


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : outlier_detection_iqr.
Describe function : 
    This function removes lines that it's data has numeric parameters and it's values are outliers.
     An outlier will be considered a value greater than Q3 + 1.5*IQR, or a value less than Q1 - 1.5*IQR.
Origin of code : 
    From our home assignments.
"""


def outlier_detection_iqr(df):
    df_copy = df.copy()
    for col in df_copy:
        if df_copy[col].dtypes != object:
            Q1 = np.percentile(df_copy[col], 20)
            Q3 = np.percentile(df_copy[col], 80)
            IQR = Q3 - Q1
            df_copy.loc[(df_copy[col] < Q1 - 1.5 * IQR) | (df_copy[col] > Q3 + 1.5 * IQR), [col]] = np.nan
            remove_corrupt_rows(df_copy)
    return df_copy
