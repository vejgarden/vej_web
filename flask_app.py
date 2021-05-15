from flask import Flask, render_template, request
import os
import glob
from sqlalchemy_declarative import WeatherRecord, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import time
from datetime import datetime
import pytz

from numpy import exp, cos, linspace
import bokeh.plotting as plt
import pandas as pd
from math import pi

from bokeh.core.properties import Dict, Int, String




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
def get_local_time(timestamp):
    local_time=tz.localize(datetime.fromtimestamp(timestamp),is_dst=True)
    return (datetime.fromtimestamp(timestamp)+local_time.utcoffset()).strftime('%Y-%m-%d %H:%M')

def get_temperature():
    #returns a list of tuples (time, temperature)
    res=session.query(WeatherRecord).with_entities(WeatherRecord.time, WeatherRecord.temperature)
    res= [(t,get_local_time(t),get_celsius(k)) for (t,k) in res][-50:]

    timestamps=[]
    timelabels=[]
    temperatures=[]

    for (timestamp,timelabel,temperature) in res:
        timestamps.append(timestamp)
        timelabels.append(timelabel)
        temperatures.append(temperature)
    return (timestamps, timelabels, temperatures)

def plot(timestamps,timelabels,temperatures):
    """Return filename of plot of the damped_vibration function."""

    #[(1620901204, '2021-05-14 10:20', 8.4), (1620902128, '2021-05-14 10:35', 8.4), (1620902941, '2021-05-14 10:49', 8.0), (1620903446, '2021-05-14 10:57', 8.0), (1620904131, '2021-05-14 11:08', 8.0)]

    #into x,y data and 2nd column as the x-axis tick
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"
    p = plt.figure(title="Christchurch Temperature", tools=TOOLS,
                   x_axis_label='Record Time', y_axis_label='Temperature("C)')

    # add a line renderer with legend and line thickness

    p.xaxis.ticker = timestamps
    p.xaxis.major_label_overrides=(dict(zip(timestamps,timelabels)))
    p.xaxis.major_label_orientation = pi/4

    p.line(timestamps,temperatures, legend_label="Temperature", line_width=2)

    from bokeh.resources import CDN
    from bokeh.embed import components
    script, div = components(p)
    head = """
        <script src="https://cdn.bokeh.org/bokeh/release/bokeh-2.3.2.min.js"
        crossorigin="anonymous"></script>
        <script type="text/javascript">
        Bokeh.set_log_level("info");
        </script>
        """
    return head, script, div

@app.route('/')
@app.route('/index')
def show_index():

    files=glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.jpg'))
    files.sort() #last one is the latest

    phist = request.args.get('phist')
    whist = request.args.get('whist')
    if phist is None:
        phist=0
    if whist is None:
        whist=0

    phist = int(phist)
    whist = int(whist)
    photo = files[phist-1]
    latest_weather=session.query(WeatherRecord).order_by(WeatherRecord.id).all()[whist-1]

    temperature = get_celsius(latest_weather.temperature)
    feels_like = get_celsius(latest_weather.feels_like)
    temp_min= get_celsius(latest_weather.temp_min)
    temp_max= get_celsius(latest_weather.temp_max)
    obs_time = latest_weather.time
    obs_time= get_local_time(obs_time)

    #obs_time = obs_time2.strftime('%Y-%m-%d %H:%M')
    weather_main = latest_weather.weather_main
    weather_desc = latest_weather.weather_desc
    humidity = latest_weather.humidity

    temperature_plot  = plot(*get_temperature())

    return render_template("index.html", user_image = photo,
            time=obs_time,
            temperature=temperature,
            temp_min=temp_min,
            temp_max=temp_max,
            feels_like=feels_like,
            weather_main=weather_main,
            weather_desc=weather_desc,
            humidity = humidity,
            phist=phist,
            whist=whist,
            temperature_plot=temperature_plot,
            )
