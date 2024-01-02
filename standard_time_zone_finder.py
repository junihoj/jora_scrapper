from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz


def get_location_timezone(location):
    geolocator = Nominatim(user_agent="timezone_finder")
    if(location == '-' or location is None or "-" in location):
        return None
    try:
        # Get the latitude and longitude of the location
        location_info = geolocator.geocode(location)
        latitude, longitude = location_info.latitude, location_info.longitude
    except AttributeError:
        return None

    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)

    if timezone_str:
        return pytz.timezone(timezone_str)
    else:
        return None

def get_location_standard_time(location):
    user_timezone = get_location_timezone(location)
    if(user_timezone):
        datetime.now(user_timezone).strftime('%Z')
    else:
        return None

