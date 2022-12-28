from CrawlingFunctions import create_soup_obj, all_hotels_parse, specific_hotel_parse, create_df

if __name__ == "__main__":
    print("-- Start --")
    tripadvisor_url_short = "https://www.tripadvisor.com/"
    tripadvisor_url = "https://www.tripadvisor.com/Hotels-g60763-N  ew_York_City_New_York-Hotels.html"
    soup = create_soup_obj(tripadvisor_url)
    all_hotels_parse(soup, tripadvisor_url_short)
    specific_hotel_parse()
    create_df()
    print("--End--")