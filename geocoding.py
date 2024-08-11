import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

def gc(city,imp):                #returns the list of tuples
    # URL of the API
    url = f'https://geocode.maps.co/search?q={city}&api_key=668911db944a0630717719hiqcf6a20'

    # Send a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the coordinates
        bounding_boxes = [[place["display_name"],[place["lat"],place["lon"]]]  for place in data if place["importance"]>=imp]

        return bounding_boxes    
    else:
        logging.error(f"Failed to fetch geocoding data. Status code: {response.status_code}")
        return ()


def rev(lat:float,lon:float):
    url = f'https://geocode.maps.co/reverse?lat={lat}&lon={lon}&api_key=668911db944a0630717719hiqcf6a20'
    response = requests.get(url)
    city=response.json()["address"]["state_district"]
    city=city.split()[0].lower()
    return city


