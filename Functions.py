import requests
from bs4 import BeautifulSoup


def all_hotels_parse(soup_obj):
    num_of_reviews = []
    hotel_url = []
    branches = soup_obj.find_all("div", {"class": "ui_column is-8 main_col allowEllipsis"})
    i = 1
    while i < 8:
        for branch in branches:
            review = branch.find("a", {"class": "review_count"}).get_text()
            num_of_reviews.append(review)
            hotel_url_1 = "https://www.tripadvisor.com/" + branch.find("a")["href"]
            hotel_url.append(hotel_url_1)
        branch_page = soup_obj.find("div", {"class": "pageNumbers"})
        next_page_url = "https://www.tripadvisor.com/" + branch_page.find("a")["href"]
        try:
            soup_obj = create_soup_obj(next_page_url, {'User-agent': 'Mozilla/5.0'})
            branches = soup_obj.find_all("div", {"class": "ui_column is-8 main_col allowEllipsis"})
        except:
            break
        i += 1
    print(num_of_reviews)
    print(hotel_url)


def create_soup_obj(url, user_agent):
    try:
        response = requests.get(url, headers=user_agent)
        print(response)
        soup_obj = BeautifulSoup(response.text, 'html.parser')
        # print(soup_obj.prettify())
        return soup_obj
    except:
        print("Error with soup object")
