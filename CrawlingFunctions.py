import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from colorama import Fore
import numpy as np

user_agent = {'User-agent': 'Mozilla/5.0'}

# Parameters for - all_hotels_parse
hotel_names = []
hotel_url = []
num_of_reviews = []

# Parameters for - specific_hotel_parse
# part 1 - general tripadvisor rate
rating_tripadvisor = []
rating_regarding_other_hotels = []

# part 2 - main tripadvisor rate
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


def create_soup_obj(url):
    try:
        response = requests.get(url, headers=user_agent)
        soup_obj = BeautifulSoup(response.text, 'html.parser')
        return soup_obj
    except:
        print(Fore.RED + "Error : couldn't create soup object!")


def all_hotels_parse(num_of_hotel_pages, soup_obj, tripadvisor_url_short):
    branches = soup_obj.find_all("div", {"class": "ui_column is-8 main_col allowEllipsis"})
    i = 1
    while i < num_of_hotel_pages:
        for branch in branches:
            review = branch.find("a", {"class": "review_count"}).get_text()
            num_of_reviews.append(review)
            hotel_name_1 = branch.find("a", {"target": "_blank"}).get_text()
            hotel_name_1_after_arrange = str(hotel_name_1).split(".")[-1].strip()
            hotel_names.append(hotel_name_1_after_arrange)
            hotel_url_1 = tripadvisor_url_short + branch.find("a")["href"]
            hotel_url.append(hotel_url_1)
        try:
            branch_page = soup_obj.find("a", attrs={"class": "nav next ui_button primary"})["href"]
            next_page_url = tripadvisor_url_short + branch_page
            print(next_page_url)
            soup_obj = create_soup_obj(next_page_url)
            branches = soup_obj.find_all("div", {"class": "ui_column is-8 main_col allowEllipsis"})
            i += 1
        except:
            print(Fore.RED + "End of pages before end of loop!")
            break


def specific_hotel_parse():
    for url in hotel_url:
        try:
            soup_obj = create_soup_obj(url)
            print(url)
        except:
            continue
        add_to_arr_2(rating_tripadvisor, find_a_number_in_string(soup_obj.find("span", {"class": "uwJeR P"})))
        add_to_arr_2(rating_regarding_other_hotels,
                     find_a_number_in_string(soup_obj.find("span", {"class": "Ci _R S4 H3 MD"})))
        string_rating = find_a_number_in_string(soup_obj.find("div", {"class": "SSDgd"}))
        if len(string_rating) < 4:
            location_rating.append(np.NaN)
            cleanliness_rating.append(np.NaN)
            service_rating.append(np.NaN)
            value_of_money.append(np.NaN)
        else:
            location_rating.append(string_rating[0])
            cleanliness_rating.append(string_rating[1])
            service_rating.append(string_rating[2])
            value_of_money.append(string_rating[3])
        str_facilities = str(soup_obj.findAll("div", attrs={"class": "ssr-init-26f"}))
        add_to_arr_1(boolean_paid_private_parking_nearby, "Paid public parking nearby", str_facilities)
        add_to_arr_1(boolean_free_high_speed_wifi, "Free High Speed Internet (WiFi)", str_facilities)
        add_to_arr_1(boolean_fitness_center, "Fitness Center with Gym / Workout Room", str_facilities)
        add_to_arr_1(boolean_air_conditioning, "Air conditioning", str_facilities)
        add_to_arr_1(boolean_minibar, "Minibar", str_facilities)
        add_to_arr_1(boolean_cable_satellite_TV, "Cable / satellite TV", str_facilities)
        add_to_arr_2(great_for_walkers_rate,
                     find_a_number_in_string(soup_obj.find("span", attrs={"class": "iVKnd fSVJN"})))
        add_to_arr_2(num_of_restaurants,
                     find_a_number_in_string(soup_obj.find("span", attrs={"class": "iVKnd Bznmz"})))
        add_to_arr_2(num_attractions,
                     find_a_number_in_string(soup_obj.find("span", {"class": "iVKnd rYxbA"})))


def add_to_arr_1(arr_name, str_facilities, search_str):
    if search_str in str_facilities:
        arr_name.append(1)
    else:
        arr_name.append(0)


def add_to_arr_2(arr_name, find_code):
    if find_code is not None:
        if type(find_code) == list and len(find_code) > 0:
            arr_name.append(find_code[0])
        elif type(find_code) == list and len(find_code) == 0:
            arr_name.append(np.NaN)
        else:
            arr_name.append(find_code)
    else:
        arr_name.append(np.NaN)


def find_a_number_in_string(s):
    return re.findall(r"[-+]?\d*\.\d+|\d+", str(s))


def create_df():
    print_arrays()
    dictionary_for_df = {"Hotel name": hotel_names, "Hotel url": hotel_url, "Number of reviews": num_of_reviews,
                         "Tripadvisor rating": rating_tripadvisor,
                         "Rating regarding other hotels in the same city": rating_regarding_other_hotels,
                         "Location rating": location_rating, "Cleanliness rating": cleanliness_rating,
                         "Service rating": service_rating, "Value of money": value_of_money,
                         "Paid private parking nearby": boolean_paid_private_parking_nearby,
                         "Free high speed wifi": boolean_free_high_speed_wifi, "Fitness_center": boolean_fitness_center,
                         "Air conditioning": boolean_air_conditioning, "Minibar": boolean_minibar,
                         "Cable satellite TV": boolean_cable_satellite_TV, "Great for walkers": great_for_walkers_rate,
                         "Number of restaurants": num_of_restaurants, "Num of attractions": num_attractions}
    return pd.DataFrame(dictionary_for_df)


def print_arrays():
    print("rating_tripadvisor " + str(len(rating_tripadvisor)))
    print(rating_tripadvisor)
    print("rating_regarding_other_hotels " + str(len(rating_regarding_other_hotels)))
    print(rating_regarding_other_hotels)
    print("location_rating " + str(len(location_rating)))
    print(location_rating)
    print("cleanliness_rating " + str(len(cleanliness_rating)))
    print(cleanliness_rating)
    print("service_rating " + str(len(service_rating)))
    print(service_rating)
    print("value_of_money " + str(len(value_of_money)))
    print(value_of_money)
    print("boolean_paid_private_parking_nearby " + str(len(boolean_paid_private_parking_nearby)))
    print(boolean_paid_private_parking_nearby)
    print("boolean_fitness_center " + str(len(boolean_fitness_center)))
    print(boolean_fitness_center)
    print("boolean_air_conditioning " + str(len(boolean_air_conditioning)))
    print(boolean_air_conditioning)
    print("boolean_minibar " + str(len(boolean_minibar)))
    print(boolean_minibar)
    print("boolean_cable_satellite_TV " + str(len(boolean_cable_satellite_TV)))
    print(boolean_cable_satellite_TV)
    print("great_for_walkers_rate " + str(len(great_for_walkers_rate)))
    print(great_for_walkers_rate)
    print("num_of_restaurants " + str(len(num_of_restaurants)))
    print(num_of_restaurants)
    print("num_attractions " + str(len(num_attractions)))
    print(num_attractions)
