#!/bin/bash
#run image recognition
IMG_DIR=/home/ubuntu/web/static/photo_tmp
cd /home/ubuntu/vej_ajh
if [ "$(ls -A $IMG_DIR)" ]; then
     echo "Take action $IMG_DIR is not Empty"
     /home/ubuntu/py385/bin/python vej_object_detection_image.py --modeldir=tflite_model/ --imagedir=$IMG_DIR
     cd $IMG_DIR
     for boxed_img in *boxed.jpg
     do
	mv $boxed_img ../photo #boxed.jpg is moved to ../photo
     done
     mv * ../photo_original #the rest are moved to photo_original
else
    echo "$IMG_DIR is Empty"
fi
#update weather
cd /home/ubuntu/vej_web
/home/ubuntu/py385/bin/python sqlalchemy_weather_update.py

