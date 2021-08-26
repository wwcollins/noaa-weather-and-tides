"""
How to find the distance between two lat-long coordinates in Python
Finding the distance between two latitude-longitude coordinates involves using the Haversine Formula. This formula takes the curvature of the Earth into consideration, which is why it is significantly more accurate than the traditional distance formula.

USE THE HAVERSINE FORMULA
The Haversine formula calculates the great-circle distance between two points. Start by calculating the change in latitude and longitude, in radians, and input the result into the Haversine formula (implemented below). Use the functions in the math library for trigonometry related calculations.

Reference:  https://www.kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python


"""

import math

def calc_distance_between_station_locations(lat,lon,lat2,lon2):
    #radius of the Earth
    Rk = 6373.0     # kilometers
    Rm = 3,958.8    # miles

    #coordinates
    lat1r = math.radians(lat)
    lon1r = math.radians(lon)

    # These values will also need to be pulled from a dict to be created to find closest weather station
    lat2r = math.radians(lat2)
    lon2r = math.radians(lon2)

    #change in coordinates
    dlon = lon2r - lon1r
    dlat = lat2r - lat1r

    #Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1r) * math.cos(lat2r) * math.sin(dlon / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = Rk * c
    distance_miles = 0.621371 * distance

    print(f'{distance} km or {distance_miles} miles')
    return distance, distance_miles


#initial lat lon vals for 2 points
lat = 52.2296756
lon = 21.0122287
lat2 = 52.406374
lon2 = 16.9251681
latlon = str(lat) + ',' + str(lon)
latlon2 = str(lat2) + ',' + str(lon2)

distance, distance_miles = calc_distance_between_station_locations(lat,lon,lat2,lon2)
print(f'The distance between latlon {latlon} and latlon {latlon2} is {distance} km or {distance_miles} miles')




"""
example OUTPUT
278.54558935106695The distance between latlon %252.2296756,21.0122287 and latlon 52.406374,16.9251681 is 278.54558935106695 km or 173.08015140066183 miles
Warning: Coordinates must be converted to radians for the calculations to be correct.
"""