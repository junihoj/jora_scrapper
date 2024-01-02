from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pytz 
from datetime import datetime
from timezonefinder import TimezoneFinder

timezone_finder = TimezoneFinder()


def get_time_zone(location):
    geolocator = Nominatim(user_agent="your_app_name")
    try:
        location_info = geolocator.geocode(location, timeout=10)
        if location_info:
            latitude, longitude = location_info.latitude, location_info.longitude
            time_zone_str = timezone_finder.timezone_at(lng=longitude, lat=latitude)
            return pytz.timezone(time_zone_str) if time_zone_str else None
        else:
            return None
    except GeocoderTimedOut as e:
        print(f"Error getting time zone for {location}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

time_zone_data = get_time_zone("usa")
print(time_zone_data)