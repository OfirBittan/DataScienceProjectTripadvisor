from CrawlingFunctions import create_soup_obj, all_hotels_parse, specific_hotel_parse, create_df, \
    create_dictionary_for_df
from CleaningFunctions import remove_duplicative, remove_corrupt_rows, outlier_detection_zscore_dist
from VisualizationFunctions import one_dim_plot, get_frequent_elements
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    print("-- Start --")
    tripadvisor_url_short = "https://www.tripadvisor.com"
    tripadvisor_urls = ["https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g187147-Paris_Ile_de_France-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g274707-Prague_Bohemia-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g186338-London_England-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g274887-Budapest_Central_Hungary-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g28930-Florida-Hotels.html"]
    # tripadvisor_urls = ["https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html"]
    for url in tripadvisor_urls:
        # CrawlingFunctions
        soup = create_soup_obj(url)
        all_hotels_parse(soup, tripadvisor_url_short)
        specific_hotel_parse()
        dictionary_for_df = create_dictionary_for_df()
        df = create_df(dictionary_for_df)

        # CleaningFunctions
        remove_duplicative(df)
        remove_corrupt_rows(df, 4)
        outlier_detection_zscore_dist(df)
        df.to_csv(r'data frame after cleaning.csv', index=False, header=True)

        # # VisualizationFunctions
        # sr = get_frequent_elements(df, "Tripadvisor rating", 3.0)
        # one_dim_plot(sr, "pie", None)
        # fig, axes = plt.subplots(1, 2, figsize=(20, 5))
        # one_dim_plot(sr, 'bar', axes[1])
    print("--End--")
