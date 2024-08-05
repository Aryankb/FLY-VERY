from fastapi import FastAPI,Depends,status,Response, HTTPException
# from schemas import City
from database import engine, SessionLocal
import tables
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from jinja2 import Template
from schemas import City


from geocoding import gc
from map import make_map
from selen import save_ss
from cluster import make_cluster


app=FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Adjust according to your frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


tables.Base.metadata.create_all(engine)   #creates all tables if not exist

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.post('/blog',status_code=status.HTTP_201_CREATED)       #status code for creating is 201      it is the response code logged
# def create(request : Blog, db: Session = Depends(get_db)):    # just write status.create , it will autocomplete
#     new_blog=tables.Blog(title=request.title,body=request.body)
#     db.add(new_blog)
#     db.commit()                                               #always commit changes when done changes in database
#     db.refresh(new_blog)
#     return new_blog


# @app.get('/blog',response_model=List[ShowBlog])                      # used response_model so that id dont get returned
# def all(db : Session=Depends(get_db)):
#     blogs=db.query(tables.Blog).all()
#     return blogs


# @app.get('/blog/{id}',status_code=200,response_model=ShowBlog)        #fetch blog corresponding to particular id
# def show(id, db: Session = Depends(get_db)):                           #used response_model so that id will not get returned along with blog
#     blog=db.query(tables.Blog).filter(tables.Blog.id==id).first()
#     if not blog:
#         # Response.status_code=status.HTTP_404_NOT_FOUND                 # if this not done, it sends a null blog with status 200
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with the {id} not available")
#     return blog
    


# @app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
# def destroy(id,db: Session = Depends(get_db)):
#     blog=db.query(tables.Blog).filter(tables.Blog.id==id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with the {id} not available')
#     blog.delete(synchronize_session=False)
#     db.commit()
#     return "done"


# @app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
# def update(id,request:Blog,db: Session = Depends(get_db)):
#     blog=db.query(tables.Blog).filter(tables.Blog.id==id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with the {id} not available')
#     else:
#         blog.update(request) #if you want to update specific column only, then take only that as post req and update({"col":"neww_val"})
#         db.commit()
#         return "updated"
    
def convert_to_coord(k,top,left):
    return [top-k[0]*(0.312/1080),left+k[1]*(0.644/1920)]

@app.post('/add_city',status_code=status.HTTP_200_OK)
def add_city(city:City, db: Session = Depends(get_db)):
    
    cityy=city.name.lower()
    c = gc(cityy,0)  # if geocode doesn't exist it returns an empty list.
    check_db = db.query(tables.City).filter((tables.City.lat==c[0][1][0]) & (tables.City.long==c[0][1][1])).first()
    # check_db=None
    Airports = gc(cityy + " airport",0.5)
    Markets = gc(cityy + " market",0)
    if not check_db or city.modify:
        if len(c):
            path = make_map(c[0][1], cityy)
            img_path = save_ss(cityy, path)
            r = make_cluster(img_path)
            new_city = tables.City(
                name=cityy,
                lat=float(c[0][1][0]),
                long=float(c[0][1][1]),
                airport=[{"id":i,"name": Airport[0], "coord": Airport[1]} for i,Airport in enumerate(Airports)],
                markets=[{"id": i, "name": Market[0], "coord": Market[1]} for i, Market in enumerate(Markets)],
                total_stations=r[0],
                stations=[{"id": i, "coord": convert_to_coord(coord,float(c[0][1][0])+0.156,float(c[0][1][1])-0.322),"valid":True} for i, coord in enumerate(r[1])]
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


    
    
    