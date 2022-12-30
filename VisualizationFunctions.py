import matplotlib.pyplot as plt


def get_frequent_elements(df, col_name):
    dfn = df.copy()
    series = dfn[col_name].value_counts()
    series = series.sort_index(ascending=True)
    return series


def one_dim_plot(sr, plot_type, axis):
    sr.plot(kind=plot_type, ax=axis)


def two_dim_plot(x, y):
    plt.scatter(x, y)
    plt.xlabel("Tripadvisor rating")
    plt.ylabel("Cleanliness rating on Tripadvisor")
