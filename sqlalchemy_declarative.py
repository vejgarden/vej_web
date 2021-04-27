import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class WeatherRecord(Base):
    __tablename__ = 'weather_records'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
#    customer_id=Column(Integer, ForeignKey('customers.id'))
    name= Column(String(20), nullable=False) #20210427_17
    time= Column(Integer) #1619502381
    city = Column(String(50))
    sunrise = Column(Integer)
    sunset = Column(Integer)
    temperature=Column(Float)
    temp_max=Column(Float)
    temp_min=Column(Float)
    feels_like=Column(Float)

    pressure=Column(Integer)
    humidity=Column(Integer)

    weather_desc=Column(String(50))
    weather_main=Column(String(20))
    clouds=Column(Float)
    wind_deg=Column(Integer)
    wind_speed=Column(Float)
    
if __name__=='__main__': 
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///static/data/weather.db')
    Base.metadata.drop_all(engine)
     
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

