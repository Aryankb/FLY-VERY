from sqlalchemy import Column, Integer, String, JSON,Float
from database import Base

class City(Base):
    __tablename__='city'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    lat=Column(Float)
    long=Column(Float)
    airport = Column(JSON)  # JSON column for airport details
    markets = Column(JSON)  # JSON column for market details
    stations = Column(JSON)  # JSON column for station details
    total_stations=Column(Integer)




