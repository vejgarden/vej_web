#!/bin/bash
/home/pi/bin/shoot >/tmp/shoot.log
img_file=`cat /tmp/shoot.log`
weather_file=/home/pi/weather_data/`basename ${img_file/.jpg/.json}`
python get_weather.py $weather_file

scp $img_file vej_ec2:/home/ubuntu/vej_web/static/img
scp $weather_file vej_ec2:/home/ubuntu/vej_web/static/weather
ssh -t vej_ec2 "cd /home/ubuntu/vej_web && /home/ubuntu/py385/bin/python sqlalchemy_weather_update.py"




