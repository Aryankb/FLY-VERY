from sqlalchemy import Column, Integer, String, JSON,Float, ForeignKey,Boolean
from database import Base
from sqlalchemy.orm import relationship   #use this to make relationships between user and products, see that part again

class City(Base):
    __tablename__='cities'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    lat=Column(Float)
    long=Column(Float)
    airport = Column(JSON)  # JSON column for airport details 
    markets = Column(JSON)  # JSON column for market details
    stations = Column(JSON)  # JSON column for station details   
    total_stations=Column(Integer)


class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)
    loc=relationship('UserLoc',back_populates='user')




class AP(Base):
    __tablename__="all_products"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)

class PO(Base):
    __tablename__='products_ordered'
    id=Column(Integer,primary_key=True,index=True)
    product_id=Column(Integer,ForeignKey('all_products.id'))
    shipped=Column(Boolean, default=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    drop_lat=Column(Float)
    drop_long=Column(Float)
    weight=Column(Float)




class UserLoc(Base):
    __tablename__='user_location'
    user_id=Column(Integer,ForeignKey('users.id'),primary_key=True)
    lat=Column(Float)
    long=Column(Float)
    city=Column(String)
    nearest_dc_id=Column(Integer)
    user=relationship('User',back_populates='loc')


