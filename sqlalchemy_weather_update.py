from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from sqlalchemy_declarative import WeatherRecord, Base
 
import os
import json
import glob

engine = create_engine('sqlite:///static/data/weather.db')
WEATHER_FOLDER = os.path.join('static','weather')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

files = glob.glob(os.path.join(WEATHER_FOLDER,'*.json'))
files.sort() #last one is the latest
print(files)

with open(files[-1]) as f:
  weather_data = json.load(f)
name=os.path.basename(files[-1]).replace(".json","")
print(name)
# Insert a Person in the person table

new_record = WeatherRecord(        
        name=name,
        time=weather_data['dt'],
        city=weather_data['name'],
        sunrise=weather_data['sys']['sunrise'],
        sunset=weather_data['sys']['sunset'],
        temperature=weather_data['main']['temp'],
        temp_max=weather_data['main']['temp_max'],
        temp_min=weather_data['main']['temp_min'],
        feels_like=weather_data['main']['feels_like'],
        pressure = weather_data['main']['pressure'],
        humidity= weather_data['main']['humidity'],
        weather_desc = weather_data['weather'][0]['description'],
        weather_main = weather_data['weather'][0]['main'],
        clouds = weather_data['clouds']['all'],
        wind_deg = weather_data['wind']['deg'],
        wind_speed = weather_data['wind']['speed']

        )

cur_data=session.query(WeatherRecord).filter(WeatherRecord.name == name and WeatherRecord.time==weather_data['dt']).all()
if len(cur_data) == 0:
    session.add(new_record)
    session.commit()
    print("Successfully inserted")
else:
    print("Duplicate data. Not inserted")

 
 
