import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from colorama import Fore
import numpy as np

"""
Students Names : Ofir Bittan and Gali Seregin
Function Name : Global parameters.
Describe function : 
    This parameters are arrays which we are going to fill with data by crawling.
Origin of code : 
    We wrote this code for the project.
"""
user_agent = {'User-agent': 'Mozilla/5.0'}
hotel_names = []
hotel_url = []
num_of_reviews = []
rating_tripadvisor = []
rating_regarding_other_hotels = []
location_rating = []
cleanliness_rating = []
service_rating = []
value_of_money = []
boolean_paid_private_parking_nearby = []
boolean_free_high_speed_wifi = []
boolean_fitness_center = []
boolean_air_conditioning = []
boolean_minibar = []
boolean_cable_satellite_TV = []
boolean_hour_front_desk = []
boolean_non_smoking_hotel = []
boolean_express_check_in_check_out = []
boolean_baggage_storage = []
boolean_housekeeping = []
boolean_safe = []
boolean_family_rooms = []
great_for_walkers_rate = []
num_of_restaurants = []
num_attractions = []
count_good_words = []
count_bad_words = []
count_total = []
"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : create_soup_obj.
Describe function : 
    This function gets url and creates sup object.
Origin of code : 
    From our home assignments.
"""


def create_soup_obj(url):
    try:
        response = requests.get(url, headers=user_agent, timeout=60)
        soup_obj = BeautifulSoup(response.text, 'html.parser')
        return soup_obj
    except:
        print(Fore.RED + "Error : couldn't create soup object!")


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : all_hotels_parse.
Describe function : 
    This function gets number of hotel pages that the user inputs.
    It crawls through the url of optional destination we peaked. 
    And gets the data into arrays. 
    Here we get :
        1. Url for specific hotel.
        2. Hotel name.
        3. Number of reviews submitted.
Origin of code : 
    We wrote this code for the project.
"""


def all_hotels_parse(num_of_hotel_pages, soup_obj, tripadvisor_url_short):
    branches = soup_obj.find_all("div", {"class": "ui_column is-8 main_col allowEllipsis"})
    i = 1
    while i < num_of_hotel_pages:
        for branch in branches:
            review = branch.find("a", {"class": "review_count"}).get_text()
            str_review = str(review).split(" ")[0]
            num_of_reviews.append(str_review)
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


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : calculate_words_good.
Describe function : 
    This function gets str of crawling from web and counts the number of 5 good connotation words we peaked
     that we saw repeating in web users comments.
Origin of code : 
    We wrote this code for the project.
"""


def calculate_words_good(str_words_from_comments):
    count_good1 = str_words_from_comments.count("good") + str_words_from_comments.count(
        "nice") + str_words_from_comments.count("liked") + str_words_from_comments.count(
        "perfect") + str_words_from_comments.count("delicious")
    return str(count_good1)


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : calculate_words_bad.
Describe function : 
    This function gets str of crawling from web and counts the number of 5 bad connotation words we peaked
     that we saw repeating in web users comments.
Origin of code : 
    We wrote this code for the project.
"""


def calculate_words_bad(str_words_from_comments):
    count_bad1 = str_words_from_comments.count("bad") + str_words_from_comments.count(
        "terrible") + str_words_from_comments.count("disappointed") + str_words_from_comments.count(
        "poor") + str_words_from_comments.count("rude")
    return str(count_bad1)


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : calculate_words_good_and_bad.
Describe function : 
    This function gets str of crawling from web and counts the number of 5 bad and good connotation words we peaked
     that we saw repeating in web users comments. 
     This function calculates and returns : (number of good words) - (number of bad words).
Origin of code : 
    We wrote this code for the project.
"""


def calculate_words_good_and_bad(str_words_from_comments):
    count_good2 = str_words_from_comments.count("good") + str_words_from_comments.count(
        "nice") + str_words_from_comments.count("liked") + str_words_from_comments.count(
        "perfect") + str_words_from_comments.count("delicious")
    count_bad2 = str_words_from_comments.count("bad") + str_words_from_comments.count(
        "terrible") + str_words_from_comments.count("disappointed") + str_words_from_comments.count(
        "poor") + str_words_from_comments.count("rude")
    count_total1 = count_good2 - count_bad2
    return str(count_total1)


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : specific_hotel_parse.
Describe function : 
    This function is going through a url array, creates soup object for every url and crawls it.
    It collects information from the web page to arrays that eventually goes to data frame.
    If there is an error in web information we add a empty data :  np.NaN.
Origin of code : 
    We wrote this code for the project.
"""


def specific_hotel_parse():
    for url in hotel_url:
        try:
            soup_obj = create_soup_obj(url)
            print(url)
            str_words_from_comments = str(soup_obj.findAll("div", attrs={"class": "YibKl MC R2 Gi z Z BB pBbQr"}))
            count_good_words.append(calculate_words_good(str_words_from_comments))
            count_bad_words.append(calculate_words_bad(str_words_from_comments))
            count_total.append(calculate_words_good_and_bad(str_words_from_comments))
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
            add_to_arr_1(boolean_hour_front_desk, "24-hour front desk", str_facilities)
            add_to_arr_1(boolean_non_smoking_hotel, "Non-smoking hotel", str_facilities)
            add_to_arr_1(boolean_express_check_in_check_out, "Express check-in / check-out", str_facilities)
            add_to_arr_1(boolean_baggage_storage, "Baggage storage", str_facilities)
            add_to_arr_1(boolean_housekeeping, "Housekeeping", str_facilities)
            add_to_arr_1(boolean_safe, "Safe", str_facilities)
            add_to_arr_1(boolean_family_rooms, "Family rooms", str_facilities)
            add_to_arr_2(great_for_walkers_rate,
                         find_a_number_in_string(soup_obj.find("span", attrs={"class": "iVKnd fSVJN"})))
            add_to_arr_2(num_of_restaurants,
                         find_a_number_in_string(soup_obj.find("span", attrs={"class": "iVKnd Bznmz"})))
            add_to_arr_2(num_attractions,
                         find_a_number_in_string(soup_obj.find("span", {"class": "iVKnd rYxbA"})))
        except:
            count_good_words.append(np.NaN)
            count_bad_words.append(np.NaN)
            count_total.append(np.NaN)
            rating_tripadvisor.append(np.NaN)
            rating_regarding_other_hotels.append(np.NaN)
            location_rating.append(np.NaN)
            cleanliness_rating.append(np.NaN)
            service_rating.append(np.NaN)
            value_of_money.append(np.NaN)
            boolean_paid_private_parking_nearby.append(np.NaN)
            boolean_free_high_speed_wifi.append(np.NaN)
            boolean_fitness_center.append(np.NaN)
            boolean_air_conditioning.append(np.NaN)
            boolean_minibar.append(np.NaN)
            boolean_cable_satellite_TV.append(np.NaN)
            boolean_hour_front_desk.append(np.NaN)
            boolean_non_smoking_hotel.append(np.NaN)
            boolean_express_check_in_check_out.append(np.NaN)
            boolean_baggage_storage.append(np.NaN)
            boolean_housekeeping.append(np.NaN)
            boolean_safe.append(np.NaN)
            boolean_family_rooms.append(np.NaN)
            great_for_walkers_rate.append(np.NaN)
            num_of_restaurants.append(np.NaN)
            num_attractions.append(np.NaN)
            continue


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : add_to_arr_1.
Describe function : 
    This function gets arr to add variables to, string from crawling, string from web page.
    It checks if a given string we want to find from the web page does exist.
    If it does we add to arr 1, else we add 0.
Origin of code : 
    We wrote this code for the project.
"""


def add_to_arr_1(arr_name, search_str, str_facilities):
    if search_str in str_facilities:
        arr_name.append("1")
    else:
        arr_name.append("0")


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : add_to_arr_2.
Describe function : 
    This function gets arr to add variables to and string from crawling.
    It adds the information we found to arr.
Origin of code : 
    We wrote this code for the project.
"""


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


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : find_a_number_in_string.
Describe function : 
    This function gets a string and extracts floating numbers from it..
    It returns an array of the number it found.
Origin of code : 
    Web url = "https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string"
"""


def find_a_number_in_string(s):
    return re.findall(r"[-+]?\d*\.\d+|\d+", str(s))


"""
Students Names : Ofir Bittan and Gali Seregin.
Function Name : create_df.
Describe function : 
    This function creates and returns data frame from the scrawling we did.
Origin of code : 
    From our home assignments.
"""


def create_df():
    dictionary_for_df = {"Hotel name": hotel_names, "Hotel url": hotel_url, "Number of reviews": num_of_reviews,
                         "Tripadvisor rating": rating_tripadvisor,
                         "Rating regarding other hotels in the same city": rating_regarding_other_hotels,
                         "Location rating": location_rating, "Cleanliness rating": cleanliness_rating,
                         "Service rating": service_rating, "Value of money": value_of_money,
                         "Paid private parking nearby": boolean_paid_private_parking_nearby,
                         "Free high speed wifi": boolean_free_high_speed_wifi, "Fitness_center": boolean_fitness_center,
                         "Air conditioning": boolean_air_conditioning, "Minibar": boolean_minibar,
                         "Cable satellite TV": boolean_cable_satellite_TV,
                         "24-hour front desk": boolean_hour_front_desk,
                         "Non-smoking hotel": boolean_non_smoking_hotel,
                         "Express check-in / check-out": boolean_express_check_in_check_out,
                         "Baggage storage": boolean_baggage_storage, "Housekeeping": boolean_housekeeping,
                         "Safe": boolean_safe, "Family rooms": boolean_family_rooms,
                         "Count good words": count_good_words, "Count bad words": count_bad_words,
                         "Count total words": count_total,
                         "Great for walkers": great_for_walkers_rate,
                         "Number of restaurants": num_of_restaurants, "Num of attractions": num_attractions}
    return pd.DataFrame(dictionary_for_df)
