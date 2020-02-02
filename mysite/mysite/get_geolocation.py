import requests
import json

ACCESS_KEY = "188691bbd66f681b0d44b39536265de4"


def get_geolocation():
    """Returns a dictionary with:
    city, country_code, country_name, ip, latitude, longitude, metro_code, region_code
    region_name, time_zone, zip_code """
    send_url = "http://api.ipstack.com/{}?access_key={}".format("204.8.158.100", ACCESS_KEY)
    r = requests.get(send_url)
    j = json.loads(r.text)
    return j