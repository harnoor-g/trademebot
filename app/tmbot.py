import json
from app.vehicle import Vehicle
from app.notify import send_email
from app.scraper import scrape_vehicle_data


VEHICLE_LIST = []
VEHICLE_MATCHES = []

REGION = '2'
LISTING_TYPE = 'private'
SORT_ORDER = 'motorslatestlistings'

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>> calls vehicle scraper to get new vehicles
#>> creates a vehicle object for each vehicle in json file
#>> checks if any vehicles match the given description 
#>> sends an email for any matching vehicles
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def run_bot(year_wanted=2000, kms_wanted=190_000, price_wanted=2000):

    vehicles = scrape_vehicle_data(REGION, LISTING_TYPE, SORT_ORDER)
    create_vehicle_instances(vehicles)
    check_for_matches(year_wanted, kms_wanted, price_wanted)
    print_vehicles()
    send_vehicle_notification()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>> cleans up json data and creates an instance of each vehicle
#>> appends vehicle objects to VEHICLE_LIST
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def create_vehicle_instances(vehicles):

    for vehicle in vehicles:
        VEHICLE_LIST.append(Vehicle(
            vehicle['vehicle_title'], 
            vehicle['odometer'], 
            vehicle['price_info'], 
            vehicle['description'], 
            vehicle['search_link']))

    if Vehicle.num_vehicles > 0:
        print(Vehicle.num_vehicles, 'new vehicle(s)')
    else:
        print('no new vehicles')


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>> checks for vehicle matches based on user defined parameters 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def check_for_matches(year_wanted, kms_wanted, price_wanted):

    for vehicle in VEHICLE_LIST:
        listing_type = vehicle.listing_type

        if listing_type == "classified" or listing_type == "auction1":

            if vehicle.buy_now_price <= price_wanted and vehicle.year >= year_wanted and vehicle.kms < kms_wanted:
                VEHICLE_MATCHES.append(vehicle)

        if listing_type == "auction2":
            continue

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>> prints vehicle information of objects in matches list
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def print_vehicles():

    for vehicle in VEHICLE_MATCHES: print(vehicle)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>> sends a text giving basic information and a search link for matched vehicles 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def send_vehicle_notification():

    for vehicle in VEHICLE_MATCHES:
        title = vehicle.title_info()
        info = vehicle.info()
        link = f"https://www.trademe.co.nz/a/{vehicle.search_link}"
        send_email(title, f"{info}\n\n{link}\n\n\n")