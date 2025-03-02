from geopy.distance import geodesic
from .models import Restaurant
from utils.coordinates import get_lat_lng_from_address

def find_nearest_restaurant(user_address):
    """
    Find the nearest restaurant to the given user address.
    """
    user_lat, user_lng = get_lat_lng_from_address(user_address)
    
    if user_lat is None or user_lng is None:
        raise ValueError("Could not determine the coordinates for the user's address.")

    nearest_restaurant = None
    shortest_distance = float('inf')  

    for restaurant in Restaurant.objects.filter(is_available=True):
        restaurant_location = (restaurant.latitude, restaurant.longitude)
        user_location = (user_lat, user_lng)

        distance = geodesic(user_location, restaurant_location).kilometers
        
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_restaurant = restaurant

    return nearest_restaurant, shortest_distance


def place_order(user, user_address):
    """
    Example function for placing an order, finding the nearest restaurant.
    """
    try:
        nearest_restaurant, distance = find_nearest_restaurant(user_address)
        print(f"Nearest restaurant is {nearest_restaurant.name}, {distance:.2f} km away.")
    except ValueError as e:
        print(f"Error: {str(e)}")
