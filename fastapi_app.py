from fastapi import FastAPI,Depends,status,Response, HTTPException
from database import engine, get_db
import tables
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from jinja2 import Template
from schemas import City,UserLogin,UserSignup, Token, CreateOrder
import hashing
import JWTtoken as tk
from datetime import timedelta


from geocoding import gc,rev
from map import make_map, make_map_satellite
from selen import save_ss,save_ss_satellite
from cluster import make_cluster
from routers import User    #use this if added any routes in User


app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust according to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


tables.Base.metadata.create_all(engine)   #creates all tables if not exist

# app.include_router(User.router)
#similarly include alll routers. we do this to make this file clean

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

@app.post('/add_city',status_code=status.HTTP_200_OK, tags=["Admin"])
def add_city(city:City, db: Session = Depends(get_db)):
    
    cityy=city.name.lower()
    c = gc(cityy,0)  # if geocode doesn't exist it returns an empty list.
    if len(c):
        check_db = db.query(tables.City).filter((tables.City.lat==c[0][1][0]) & (tables.City.long==c[0][1][1]))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{city} not found")
    
    # Markets = gc(cityy + " market",0)
    if not check_db.first():
        if len(c):
            path = make_map(c[0][1], cityy)
            satellite_path=make_map_satellite(c[0][1],cityy)
            img_path = save_ss(cityy, path)
            sat_img=save_ss_satellite(cityy,satellite_path)
            r = make_cluster(img_path,sat_img)                               
            Airports = gc(cityy + " airport",0.4)
            # dont ADD those stations which are very far from house clusters
            # in front end, dark green -> satation+dc, green -> only dc, blue -> only station, grey -> locations within airport range, airport circle -> red
            # mark stations within airport reach here only
            # in frontend, after adding city, (show a local map) when admin makes changes, and gives a new set of valid stations, handle it in /approved route (put req)
            # also mark approved ones in the global map (inside approved route)
            new_city = tables.City(                                    
                name=cityy,                                     
                lat=float(c[0][1][0]),                                
                long=float(c[0][1][1]),                               
                airport=[{"id":i,"name": Airport[0], "coord": Airport[1]} for i,Airport in enumerate(Airports)],
                # markets=[{"id": i, "name": Market[0], "coord": Market[1]} for i, Market in enumerate(Markets)],
                total_stations=r[0],
                stations=[{"id": i, "coord": convert_to_coord(coord,float(c[0][1][0])+0.156,float(c[0][1][1])-0.322),"station":True,"DC":False} for i, coord in enumerate(r[1])]
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










@app.delete('/city/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["Admin"])
def destroy(id,db: Session = Depends(get_db)):
    blog=db.query(tables.City).filter(tables.City.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'city with the id : {id} not available')
    blog.delete(synchronize_session=False)
    db.commit()
    
    return "done"







@app.post('/UserSignup',status_code=status.HTTP_201_CREATED, tags=["Auth"])
def signup(user: UserSignup,db: Session = Depends(get_db)):
    check_db = db.query(tables.User).filter(tables.User.email==user.email).first()
    if not check_db:

        new_user=tables.User(name=user.name,                                        
                             email=user.email,
                             password=hashing.hash.bcrypt(user.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return "Signup Successful"                             # dont return anything. just dislplay signup successful / acc already exist and redirect to login page
    else:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail=f"Account with email : {user.email} already exist")







@app.post("/UserLogin",status_code=status.HTTP_200_OK, tags=["Auth"])
def login(user :UserLogin,db: Session = Depends(get_db)):
    check_db = db.query(tables.User).filter(tables.User.email==user.email).first()
    if not check_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Please sign up first.")
    if not hashing.hash.verify(user.password,check_db.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Incorrect Password.")
    
    # access_token = tk.create_access_token(
    #     data={"sub": user.email}                                       # return username , city name
    # )
    # return Token(access_token=access_token, token_type="bearer")

    user_city=rev(user.lat,user.long)
    user_city=user_city.lower()
    # check_city=db.query(tables.City).filter(tables.City.name==user_city).first()
    # if not check_city:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"City : {user_city} not available for delivery")
    # insert coordinates into user loc table (id,coord)
    new=tables.UserLoc(user_id=check_db.id,lat=user.lat,long=user.long,city=user_city)
    db.add(new)
    db.commit()
    db.refresh(new)

    
    return {"name":check_db.name,
            "city": user_city,
            "id":check_db.id
            }



# #add prducts online shopping table (manually do it or by scrapping)
# app.get # show all products in online shopping table



@app.put('/Current_Loc/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["User"])
def update(id,lat:float,long:float,db: Session = Depends(get_db)):
    
    # before this display please choose drop location a wide and open area -> terrace or road or open ground
    crr=db.query(tables.UserLoc).filter(tables.UserLoc.user_id==id)

    user_city=rev(lat,long)
    check_city=db.query(tables.City).filter(tables.City.name==user_city).first()

    # mark the nearest dc in the userLoc table
    dcs=[i for i in check_city["stations"] if i["DC"]==True]
    dist=float("inf")
    nearest_dc=-1
    for i in dcs:
        if dist>(i["coord"][0]-lat)**2+(i["coord"][1]-long)**2:
            dist=(i["coord"][0]-lat)**2+(i["coord"][1]-long)**2
            nearest_dc=i["id"]
    if not check_city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"City : {user_city} not available for delivery")

    if not nearest_dc==-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"City : {user_city} dont have a distribution centre")
    
    
    crr.update({"lat":lat,"long":long,"city":user_city,"nearest_dc_id":nearest_dc})
    db.commit()
    
    return {"city":user_city}  




# @app.post("/createOrder",status_code=status.HTTP_201_CREATED,tags=["User"])
# def order(user_id:CreateOrder,db: Session = Depends(get_db)):
#     pass


# @app.post(qr,dc id, city id) # scan 
# add weight here, directly on dc table (make dc table for every dc in mongodb, with col assigned_drone= Tre or false)



# @app.get()  # show all cities with their dc on map


# @app.get()  # show particular city with their dc on map, airport



    










    #/login route ->  post req email, pass, lat, long (find out region by reverse geocode). if auth success -> show the region in ##COPY OF## global map. user will be able to mark his location on that map
    # keep an option of shop online . redirect to a page where web scrapped items from any shopping site. user can make order -> POST REQ() on route /create_order 

    #there will be a global map which saves all approved, marked stations, (when clicked on a store, it redirects to the new page with available items in that store)







    # extra -> user review and return products, accordingly suggest to keep stock of frequently ordered items in a city
    #collect data over a year and suggest season wise stocking for a city
    # try to make recommendation system for user based on age , searches , gender
    # very extras --> google auth, make payments, loading percent, use better geocoding api
    # how to handle many users simult? caching?


# Race Conditions: In poorly designed systems, simultaneous execution of code might lead to race conditions where the outcome depends on the sequence of execution. This is usually mitigated through careful coding practices and using synchronization mechanisms.
# Resource Limits: If too many users access the system simultaneously, it could lead to resource exhaustion (e.g., CPU, memory, database connections). To handle this, systems often implement rate limiting, auto-scaling, or queuing mechanisms.
