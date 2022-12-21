from Functions import create_soup_obj, all_hotels_parse

if __name__ == "_main_":
    tripadvisor_url = "https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html"
    soup = create_soup_obj(tripadvisor_url, {'User-agent': 'Mozilla/5.0'})
    all_hotels_parse(soup)