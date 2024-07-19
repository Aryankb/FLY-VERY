import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

def gc(city):                #returns the list of tuples
    # URL of the API
    url = f'https://geocode.maps.co/search?q={city}&api_key=668911db944a0630717719hiqcf6a20'

    # Send a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the coordinates
        bounding_boxes = [(place["display_name"],[place["lat"],place["lon"]]) for place in data]

        return bounding_boxes    
    else:
        logging.error(f"Failed to fetch geocoding data. Status code: {response.status_code}")
        return []



