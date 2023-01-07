import matplotlib.pyplot as plt

"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : get_frequent_elements.
Describe function : 
    This function gets data frame and column name and returns it as a series object.
Origin of code : 
    From our home assignments.
"""


def get_frequent_elements(df, col_name):
    dfn = df.copy()
    series = dfn[col_name].value_counts()
    series = series.sort_index(ascending=True)
    return series


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : one_dim_plot.
Describe function : 
    This function gets a series, plot type and axis 0/1 and creates a plot.
Origin of code : 
    From our home assignments.
"""


def one_dim_plot(sr, plot_type, axis):
    sr.plot(kind=plot_type, ax=axis)


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : two_dim_plot.
Describe function : 
    This function gets data frame and creates a scatter plot.
Origin of code : 
    We wrote this code for the project.
"""


def two_dim_plot(x, y):
    plt.scatter(x, y)
    plt.xlabel("Tripadvisor rating")
    plt.ylabel("Cleanliness rating on Tripadvisor")
