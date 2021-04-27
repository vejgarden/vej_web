from flask import Flask, render_template
import os
import glob
from sqlalchemy_declarative import WeatherRecord, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import time
from datetime import datetime
import pytz
tz = pytz.timezone('Pacific/Auckland')

IMG_FOLDER = os.path.join('static', 'photo')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

engine=create_engine('sqlite:///static/data/weather.db')
Base.metadata.bind = engine
DBSession=sessionmaker()
DBSession.bind=engine
session=DBSession()

def get_celsius(kelvin):
    return round(kelvin-273.15,1)

@app.route('/')
@app.route('/index')
def show_index():
    files=glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.jpg'))
    files.sort() #last one is the latest
    latest_weather=session.query(WeatherRecord).order_by(WeatherRecord.id).all()[-1]
    temperature = get_celsius(latest_weather.temperature)
    feels_like = get_celsius(latest_weather.feels_like)
    temp_min= get_celsius(latest_weather.temp_min)
    temp_max= get_celsius(latest_weather.temp_max)
    obs_time = latest_weather.time
    nz_time=tz.localize(datetime.fromtimestamp(obs_time),is_dst=True)
    obs_time= (datetime.fromtimestamp(obs_time)+nz_time.utcoffset()).strftime('%Y-%m-%d %H:%M')

    #obs_time = obs_time2.strftime('%Y-%m-%d %H:%M')
    weather_main = latest_weather.weather_main
    weather_desc = latest_weather.weather_desc
    humidity = latest_weather.humidity


    return render_template("index.html", user_image = files[-1],
            time=obs_time,
            temperature=temperature,
            temp_min=temp_min,
            temp_max=temp_max,
            feels_like=feels_like,
            weather_main=weather_main,
            weather_desc=weather_desc,
            humidity = humidity,
            )
