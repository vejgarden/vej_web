import requests
from pprint import pprint
import sys
import os
import json
from config import API_key
 
# This stores the url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
# This will ask the user to enter city ID
#city_id = input("Enter a city ID : ")
city_id="2192362"
 
# This is final url. This is concatenation of base_url, API_key and city_id
final_url = base_url + "appid=" + API_key + "&id=" + city_id

if __name__ =="__main__":
    if len(sys.argv)!=2:
        print("Usage: {} output_path".format(sys.argv[0]))
        sys.exit()

    outpath=sys.argv[1]
    if os.path.isdir(outpath) or not os.path.isdir(os.path.abspath(os.path.dirname(outpath))):
        print("Error: fix output path {}".format(outpath))
        sys.exit()

    # this variable contain the JSON data which the API returns
    weather_data = requests.get(final_url).json()
     
    # JSON data is difficult to visualize, so you need to pretty print 
    pprint(weather_data)

    with open(outpath, "w") as f:
        json.dump(weather_data, f, indent = 6)
