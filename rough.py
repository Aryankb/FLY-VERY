from database import engine, SessionLocal
import tables
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException,status

from geocoding import gc
from map import make_map
from selen import save_ss
from cluster import make_cluster
# import geocoder
# import requests
# g = geocoder.ip('me')
# url = f'https://geocode.maps.co/reverse?lat={(g.latlng)[0]}&lon={(g.latlng)[1]}&api_key=668911db944a0630717719hiqcf6a20'
# response = requests.get(url)
# city=response.json()["address"]["city_district"]
# print(city)
tables.Base.metadata.create_all(engine)   #creates all tables if not exist


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_city(city:str, db: Session = Depends(get_db)):
    city=city.lower()
    c = gc(city)  # if geocode doesn't exist it returns an empty list.
    check_db = db.query(tables.City).filter(tables.City.geo_coord == ",".join(list(map(str,c[0][1])))).first()
    airport = gc(city + " airport")
    markets = gc(city + " market")
    if not check_db:
        if len(c):
            path = make_map(c[0][1], city)
            img_path = save_ss(city, path)
            r = make_cluster(img_path)
            new_city = tables.City(
                name=city,
                geo_coord=",".join(list(map(str,c[0][1]))),
                airport={"name": airport[0][0], "coord": airport[0][1]},
                markets=[{"id": i, "name": market[0], "coord": market[1]} for i, market in enumerate(markets)],
                total_stations=r[0],
                stations=[{"id": i, "coord": coord} for i, coord in enumerate(r[1])]
            )
            db.add(new_city)
            db.commit()
            db.refresh(new_city)
            
            # Return the city data
            return new_city
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{city} not found")
    else:
        # Return the city data
        return check_db
    

import folium
my_map1 = folium.Map(location=[28.6273928,77.1716954], zoom_start=12)
# tile = folium.TileLayer(
#         tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#         attr = 'Esri',
#         name = 'Esri Satellite',
#         overlay = False,
#         control = True
#        ).add_to(my_map1)
my_map1.save("map.html")