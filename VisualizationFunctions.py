import matplotlib.pyplot as plt


def get_frequent_elements(df, col_name, num_top_elements):
    dfn = df.copy()
    series = dfn[col_name].value_counts()[:num_top_elements]
    series = series.sort_index(ascending=True)
    return series


def one_dim_plot(sr, plot_type, axis):
    if axis is None:
        sr.plot(kind=plot_type)
    else:
        sr.plot(kind=plot_type, ax=axis)
    plt.savefig(plot_type + ".png")
