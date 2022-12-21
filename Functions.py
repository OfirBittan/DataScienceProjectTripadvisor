import requests
from bs4 import BeautifulSoup
import re

user_agent = {'User-agent': 'Mozilla/5.0'}

# Parameters for - all_hotels_parse
num_of_reviews = []
hotel_url = []

# Parameters for - specific_hotel_parse
# part 1
rating_tripadvisor = []
rating_regarding_other_hotels = []

# part 2
location_rating = []
cleanliness_rating = []
service_rating = []
value_of_money = []

# part 3 - Property amenities
boolean_paid_private_parking_nearby = []
boolean_free_high_speed_wifi = []
boolean_fitness_center = []

# part 4 - Room features
boolean_air_conditioning = []
boolean_minibar = []
boolean_cable_satellite_TV = []

# part 5 - Great for walkers, Restaurants, Attractions
great_for_walkers_rate = []
num_of_restaurants = []
num_attractions = []


def print_arrays():
    print("rating_tripadvisor")
    print(rating_tripadvisor)
    print("rating_regarding_other_hotels")
    print(rating_regarding_other_hotels)
    print("location_rating")
    print(location_rating)
    print("cleanliness_rating")
    print(cleanliness_rating)
    print("service_rating")
    print(service_rating)
    print("value_of_money")
    print(value_of_money)
    print("boolean_paid_private_parking_nearby")
    print(boolean_paid_private_parking_nearby)
    print("boolean_free_high_speed_wifi")
    print(boolean_free_high_speed_wifi)
    print("boolean_fitness_center")
    print(boolean_fitness_center)
    print("boolean_air_conditioning")
    print(boolean_air_conditioning)
    print("boolean_minibar")
    print(boolean_minibar)
    print("boolean_cable_satellite_TV")
    print(boolean_cable_satellite_TV)
    print("great_for_walkers_rate")
    print(great_for_walkers_rate)
    print("num_of_restaurants")
    print(num_of_restaurants)
    print("num_attractions")
    print(num_attractions)


def build_df():
    return None


def find_a_number_in_string(s):
    # In string rating added function that gets floats out of the string
    return re.findall(r"[-+]?\d*\.\d+|\d+", str(s))


def specific_hotel_parse():
    for url in hotel_url:
        try:
            soup_obj = create_soup_obj(url)
        except:
            continue
        add_to_arr(rating_tripadvisor, soup_obj.find("span", {"class": "uwJeR P"}).get_text())
        add_to_arr(rating_regarding_other_hotels, soup_obj.find("span", {"class": "Ci _R S4 H3 MD"}).get_text())
        string_rating = find_a_number_in_string(soup_obj.find("div", {"class": "SSDgd"}).get_text())
        location_rating.append(string_rating[0])
        cleanliness_rating.append(string_rating[1])
        service_rating.append(string_rating[2])
        value_of_money.append(string_rating[3])
        string_facilities = str(soup_obj.findAll("div", attrs={"class": "ssr-init-26f"}))
        if "Paid public parking nearby" in string_facilities:
            boolean_paid_private_parking_nearby.append("1")
        else:
            boolean_paid_private_parking_nearby.append("0")
        if "Free High Speed Internet (WiFi)" in string_facilities:
            boolean_free_high_speed_wifi.append("1")
        else:
            boolean_free_high_speed_wifi.append("0")
        if "Fitness Center with Gym / Workout Room" in string_facilities:
            boolean_fitness_center.append("1")
        else:
            boolean_fitness_center.append("0")
        if "Air conditioning" in string_facilities:
            boolean_air_conditioning.append("1")
        else:
            boolean_air_conditioning.append("0")
        if "Minibar" in string_facilities:
            boolean_minibar.append("1")
        else:
            boolean_minibar.append("0")
        if "Cable / satellite TV" in string_facilities:
            boolean_cable_satellite_TV.append("1")
        else:
            boolean_cable_satellite_TV.append("0")
        add_to_arr(great_for_walkers_rate,
                   find_a_number_in_string(soup_obj.find("span", attrs={"class": "iVKnd fSVJN"})))
        add_to_arr(num_of_restaurants, find_a_number_in_string(soup_obj.find("span", attrs={"class": "iVKnd Bznmz"})))
        add_to_arr(num_attractions, find_a_number_in_string(soup_obj.find("span", {"class": "iVKnd rYxbA"}).get_text()))
        print_arrays()


def add_to_arr(arr_name, find_code):
    try:
        return arr_name.append(find_code)
    except:
        return "No Parameter"


def all_hotels_parse(soup_obj, tripadvisor_url_short):
    branches = soup_obj.find_all("div", {"class": "ui_column is-8 main_col allowEllipsis"})
    i = 1
    while i < 10:
        for branch in branches:
            review = branch.find("a", {"class": "review_count"}).get_text()
            num_of_reviews.append(review)
            hotel_url_1 = tripadvisor_url_short + branch.find("a")["href"]
            hotel_url.append(hotel_url_1)
        branch_page = soup_obj.find("div", {"class": "pageNumbers"})
        next_page_url = tripadvisor_url_short + branch_page.find("a")["href"]
        try:
            soup_obj = create_soup_obj(next_page_url)
            branches = soup_obj.find_all("div", {"class": "ui_column is-8 main_col allowEllipsis"})
        except:
            print("End of pages before end of loop!")
            break
        i += 1
    # print(num_of_reviews)
    print(hotel_url)


def create_soup_obj(url):
    try:
        response = requests.get(url, headers=user_agent)
        print(response)
        soup_obj = BeautifulSoup(response.text, 'html.parser')
        # print(soup_obj.prettify())
        return soup_obj
    except:
        print("Error : couldn't create soup object!")
