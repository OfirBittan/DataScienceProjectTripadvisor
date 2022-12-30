from CrawlingFunctions import create_soup_obj, all_hotels_parse, specific_hotel_parse, create_df
from CleaningFunctions import remove_duplicative, remove_corrupt_rows, outlier_detection_zscore_dist
from VisualizationFunctions import one_dim_plot, get_frequent_elements, two_dim_plot
import matplotlib.pyplot as plt
from MachineLearningFunctions import load_dataset, transfer_str_to_numeric_vals, split_to_train_and_test, \
    find_best_model

if __name__ == "__main__":
    print("-- Start --")
    # num_of_hotel_pages = int(input("How many pages do you want to crawl? "))

    # tripadvisor_url_short = "https://www.tripadvisor.com"
    # tripadvisor_urls = ["https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html",
    #                     "https://www.tripadvisor.com/Hotels-g187147-Paris_Ile_de_France-Hotels.html",
    #                     "https://www.tripadvisor.com/Hotels-g274707-Prague_Bohemia-Hotels.html",
    #                     "https://www.tripadvisor.com/Hotels-g186338-London_England-Hotels.html",
    #                     "https://www.tripadvisor.com/Hotels-g274887-Budapest_Central_Hungary-Hotels.html",
    #                     "https://www.tripadvisor.com/Hotels-g28930-Florida-Hotels.html"]
    # tripadvisor_urls = ["https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html"]

    # print("-- Crawling --")
    # for url in tripadvisor_urls:
    #     soup = create_soup_obj(url)
    #     all_hotels_parse(num_of_hotel_pages, soup, tripadvisor_url_short)
    # specific_hotel_parse()
    # df = create_df()
    # df.to_csv(r'data frame before cleaning.csv', index=False, header=True)
    #
    # print("-- Cleaning --")
    # remove_duplicative(df)
    # remove_corrupt_rows(df)
    # df = outlier_detection_zscore_dist(df)
    # df.to_csv(r'data frame after cleaning.csv', index=False, header=True)
    #
    # print("-- Visualization --")
    # sr = get_frequent_elements(df, "Tripadvisor rating")
    # fig, axes = plt.subplots(1, 2, figsize=(20, 5))
    # one_dim_plot(sr, "pie", axes[0])
    # one_dim_plot(sr, "bar", axes[1])
    # plt.savefig("OneDimPlot.png")
    # plt.close()
    # two_dim_plot(df["Tripadvisor rating"], df["Cleanliness rating"])
    # plt.savefig("TwoDimPlot.png")
    # plt.close()

    print("-- Machine Learning --")
    file_name = "data frame after cleaning - old for test.csv"
    test_ratio, rand_state = 0.2, 42
    max_dep = 4
    min_smpl_splt = 5
    category_col_name = 'class'
    raw_dataset = load_dataset(file_name)
    dataset = transfer_str_to_numeric_vals(raw_dataset)
    X_train, X_test, y_train, y_test = split_to_train_and_test(dataset, category_col_name, test_ratio, rand_state)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    best_clf, best_recall_val = find_best_model(X_train, y_train, max_dep, min_smpl_splt)
    print(str(best_clf))
    print(str(best_recall_val))

    print("--End--")
