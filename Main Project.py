from CrawlingFunctions import create_soup_obj, all_hotels_parse, specific_hotel_parse, create_df
from CleaningFunctions import remove_duplicative, remove_corrupt_rows, outlier_detection_iqr
from VisualizationFunctions import one_dim_plot, get_frequent_elements, two_dim_plot
import matplotlib.pyplot as plt
from MachineLearningFunctions import split_to_train_and_test, get_data_ready, check_eda_method, \
    transfer_str_to_numeric_vals

"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : __main__.
Describe function : 
    This function is the main function of the project.
    It calls all the functions needed by the order of the assignment given.
Origin of code : 
    We wrote this code for the project.
"""
if __name__ == "__main__":
    print("-- Start --")
    num_of_hotel_pages = int(input("How many pages do you want to crawl? "))

    tripadvisor_url_short = "https://www.tripadvisor.com"
    tripadvisor_urls = ["https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g187147-Paris_Ile_de_France-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g274707-Prague_Bohemia-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g186338-London_England-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g274887-Budapest_Central_Hungary-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g28930-Florida-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g188045-Switzerland-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g187275-Germany-Hotels.html",
                        "https://www.tripadvisor.com/Hotels-g255060-Sydney_New_South_Wales-Hotels.html"]

    print("-- Crawling --")
    for url in tripadvisor_urls:
        soup = create_soup_obj(url)
        all_hotels_parse(num_of_hotel_pages, soup, tripadvisor_url_short)
    specific_hotel_parse()
    df = create_df()
    df.to_csv(r'dataFrameBeforeCleaning.csv', index=False, header=True)

    print("-- Cleaning --")
    df = get_data_ready("dataFrameBeforeCleaning.csv")
    remove_duplicative(df)
    remove_corrupt_rows(df)
    df = outlier_detection_iqr(df)
    df.to_csv(r'dataFrameAfterCleaning.csv', index=False, header=True)

    print("-- Visualization --")
    sr = get_frequent_elements(df, "Tripadvisor rating")
    fig, axes = plt.subplots(1, 2, figsize=(20, 5))
    one_dim_plot(sr, "pie", axes[0])
    one_dim_plot(sr, "bar", axes[1])
    plt.savefig("one_dim_plot.png")
    plt.close()
    two_dim_plot(df["Tripadvisor rating"], df["Cleanliness rating"])
    plt.savefig("two_dim_plot.png")
    plt.close()

    print("-- Machine Learning --")
    df = transfer_str_to_numeric_vals(df)
    test_ratio, rand_state = 0.2, 42
    X_train, X_test, y_train, y_test = split_to_train_and_test(df, "Tripadvisor rating", test_ratio, rand_state)
    check_eda_method(X_train, X_test, y_train, y_test)
    print("--The End--")
