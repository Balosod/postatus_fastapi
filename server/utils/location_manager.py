
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="MyApp")


def get_location(lat,lon):
    try:
        coordinates = f"{lat},{lon}"
        location = geolocator.reverse(coordinates)
        address = location.raw['address']
        return address
    except:
        return None
    