import requests 
from bs4 import BeautifulSoup 
import json
from time import sleep


def scrape_vehicle_data(region, listing, sort_order):
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>> load the data from the url and parse the response content to bs 
#>> search parameters: region - Auckland, listing type - private, sort order - latest listings, page - 1
#>> get all the unique identifiers from identifiers.txt  
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    url = f"https://www.trademe.co.nz/a/motors/cars/search?user_region={region}&listing_type={listing}&sort_order={sort_order}&page=1"
    try:
        response = requests.get(url, timeout=6)
    except:
        sleep(1)
        response = requests.get(url, timeout=6)
        while response.status_code != 200:
            sleep(1)
            response = requests.get(url, timeout=6)
    content = BeautifulSoup(response.content, "html.parser")

    with open("./data/identifiers.txt") as data:
        identifiers = json.load(data)
    if len(identifiers) > 30:
        del identifiers[:len(identifiers)-29]

    new_vehicles = []

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>> use the unique id to check if vehicle has been processed previously 
#>> for each of the search cards from the parsed content, find the relevent information
#>> info includes: vehicle title, basic details, odometer, price information, and link path 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    for vehicle in content.findAll("div", attrs={"class":"tm-motors-search-card__wrapper"}):
 
        unique_id = vehicle.find("div", attrs={"class":"tm-motors-search-card__location"}).attrs["id"]
        unique_id = unique_id.split("-")[1]

        if unique_id not in identifiers:
            try:
                vehicle_title = vehicle.find("div", attrs={"class":"tm-motors-search-card__title"}).text
                desc = vehicle.find("span", attrs={"class":"tm-motors-search-card__engine-details"}).text

                try:
                    odometer = vehicle.find("span", attrs={"class":"tm-motors-search-card__body-odometer"}).text

                except AttributeError:
                    odometer = "0km"
                price_info = vehicle.find("div", attrs={"class":"tm-motors-search-card__price-details"}).text
                url_link = vehicle.find("a", attrs={"class":"tm-motors-search-card__link"}).attrs["href"]

            except AttributeError:
                continue

            vehicle_obj = {
                "vehicle_title": vehicle_title.strip(), 
                "odometer": odometer.strip(), 
                "description": desc.strip(), 
                "price_info": price_info.strip(),
                "search_link": url_link.strip()
                }

            new_vehicles.append(vehicle_obj)
            identifiers.append(unique_id)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>> store unique identifiers in a text file to identify duplicate listings
#>> return new vehicles
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 

    with open("./data/identifiers.txt", "w") as id_out:
        json.dump(identifiers, id_out)

    with open('./data/vehicle-data.json', 'w') as vehicle_data:
        json.dump(new_vehicles, vehicle_data)

    return new_vehicles