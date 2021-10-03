import requests
from bs4 import BeautifulSoup
import pandas 

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore//?page="
page_num_MAX = 3

for page_num in range(1, page_num_MAX):
    req = requests.get(oyo_url + str(page_num)) 
    content = req.content
    soup = BeautifulSoup(content, "html.parser")

    all_hotels = soup.find_all("div", {"class": "hotelCardListing"})

    scraped_into_list = []

    for hotel in all_hotels:
         hotel_dict = {}
         hotel_dict["name"] = hotel.find("h3", {"class": "ListinghotelDescription_hotelName"}).text
    
         hotel_dict["address"]= hotel.find("span", {"itemprop": "streetAdress"}).text
    
         hotel_dict["price"] = hotel.find("span", {"class": "ListingPrice__finalPrice"}).text
         try:
            hotel_dict["rating"] = hotel.find("span", {"class": "hotelRating__ratingSummary"}).text
         except AttributeError:
            pass
    
    
    parent_amenities_element = hotel.find("div", {"class": "amenityWrapper"})
    
    amenities_list = []
    
    for amenity in parent_amenities_element.find_all("div", {"class": "amenityWrapper__amnity"}):
        amenities_list.append(amenity.find("span", {"class": "d-body-smd-textEllipsis"}).text.strip())
    
    hotel_dict["amenities"] = ', '.join(amenities_list[:-1])
    
    scraped_into_list.append(hotel_dict)

dataFrame = pandas.DataFrame(scraped_into_list)
dataFrame.to_csv("Oyo.csv")
