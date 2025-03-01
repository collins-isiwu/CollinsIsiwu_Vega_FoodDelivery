from opencage.geocoder import OpenCageGeocode
from django.conf import settings

def get_lat_lng_from_address(address):
    """
    Convert an address to latitude and longitude using OpenCage API.
    """
    key = settings.OPENCAGE_API_KEY
    geocoder = OpenCageGeocode(key)

    result = geocoder.geocode(address)
    
    if result and len(result):
        return result[0]['geometry']['lat'], result[0]['geometry']['lng']
    
    return None, None  
