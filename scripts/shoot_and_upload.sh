#!/bin/bash
/home/pi/vej_web/scripts/shoot >/tmp/shoot.log
img_file=`cat /tmp/shoot.log`
weather_file=/home/pi/weather_data/`basename ${img_file/.jpg/.json}`
python /home/pi/vej_web/scripts/get_weather.py $weather_file

hour=`date +"%H"`
#if [ $hour -le 17 ] && [ $hour -ge 07 ]
#then
#	scp $img_file vej_ec2:/home/ubuntu/vej_web/static/photo
#fi
scp $img_file vej_ec2:/home/ubuntu/vej_web/static/photo_tmp
scp $weather_file vej_ec2:/home/ubuntu/vej_web/static/weather
ssh -t vej_ec2 "cd /home/ubuntu/vej_web && /bin/bash update_server.sh"




