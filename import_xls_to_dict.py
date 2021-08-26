# pip install xlrd
# pip install pandas
# pip install openpyxl
# pip install plotly (for geomap image - see other py script example TBD

import pandas as pd
import json
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

    # print(f'{distance} km or {distance_miles} miles')
    return distance, distance_miles

def get_closets_station(lat,lon):
    filepath = 'StationsDataTest.xlsx'

    # Create the DataFrame - this can be moved to another method since this really needs to be read from excel only once then
    # accessed via the exported json file into a df.  Could also use a boolean here to perform an excel source refresh
    
    df = pd.read_excel(filepath)
    print (df)

    dfd = df.to_dict()
    dfj = df.to_json(orient='split')

    print(dfj)

    # create JSON object from JSON text
    json_string = dfj
    jobj = json.loads(json_string)

    least_distance = "1000000000"
    least_distance_loc = []

    for L in range(100000):
        #print(jobj['data'][L])
        try:
            closest_list = jobj['data'][L]
        except Exception as e:
            print('...end of entries to evaluate')
            break
       
        #print(jobj['data'][L][0])
        #print(jobj['data'][L][1])
        #print(jobj['data'][L][2]) # station ID
        #print(jobj['data'][L][3])
        #print(jobj['data'][L][4])
        
        station_id = jobj['data'][L][2]
        
        lat2 = jobj['data'][L][3]
        lon2 = jobj['data'][L][4]
        latlon = str(lat) + ',' + str(lon)
        latlon2 = str(lat2) + ',' + str(lon2)
        
        #calculate distance between this lat lon above and target lat lon
        distance, distance_miles = calc_distance_between_station_locations(lat,lon,lat2,lon2)
        # print(f'The distance between latlon {latlon} and latlon {latlon2} is {distance} km or {distance_miles} miles')
        
        distance = float(distance)
        least_distance = float(least_distance)
        
        if distance < least_distance:
            print(f'...found closer station {station_id} ')
            print(f'...current station distance is {float(distance)} vs previous at {float(least_distance)}')
            least_distance = float(distance) # set least to new lower val
            least_distance_loc = jobj['data'][L]
            least_distance_loc.append(distance)
        else:
            print(f'... station {station_id} is not closer ')

    print()
    print(f'Closest station information {least_distance_loc} and closest station is {least_distance_loc[2]}') 
    print(f'Target location and station {least_distance_loc[2]} are ~{round(least_distance_loc[-1],1)}km apart')
    
    # Export Pandas DataFrame to JSON File
    df.to_json(r'StationsDataTest.json',orient='split')
    
    return station_id, least_distance_loc # station ID and return list for closest location data


# Test
# now test loop and compare calculate lat lon distance from target, find smallest, match with station id
# California	Imperial Beach	9410120	32.5783	-117.135	Subordinate
# Corpus Christi, TX  Latitude: 27.800583 Longitude: -97.396378
lat = 27.800583
lon = -97.396378

station_id, least_distance_loc = get_closets_station(lat,lon)
print(f'returned values from get_closets_station are closest station id {station_id} and data list {least_distance_loc}')

quit()

least_distance = "1000000000"
least_distance_loc = []

for L in range(100000):
    #print(jobj['data'][L])
    try:
        closest_list = jobj['data'][L]
    except Exception as e:
        print('...end of entries to evaluate')
        break
   
    #print(jobj['data'][L][0])
    #print(jobj['data'][L][1])
    #print(jobj['data'][L][2]) # station ID
    #print(jobj['data'][L][3])
    #print(jobj['data'][L][4])
    
    station_id = jobj['data'][L][2]
    
    lat2 = jobj['data'][L][3]
    lon2 = jobj['data'][L][4]
    latlon = str(lat) + ',' + str(lon)
    latlon2 = str(lat2) + ',' + str(lon2)
    
    #calculate distance between this lat lon above and target lat lon
    distance, distance_miles = calc_distance_between_station_locations(lat,lon,lat2,lon2)
    # print(f'The distance between latlon {latlon} and latlon {latlon2} is {distance} km or {distance_miles} miles')
    
    distance = float(distance)
    least_distance = float(least_distance)
    
    if distance < least_distance:
        print(f'...found closer station {station_id} ')
        print(f'...current station distance is {float(distance)} vs previous at {float(least_distance)}')
        least_distance = float(distance) # set least to new lower val
        least_distance_loc = jobj['data'][L]
        least_distance_loc.append(distance)
    else:
        print(f'... station {station_id} is not closer ')

print()
print(f'Closest station information {least_distance_loc} and closest station is {least_distance_loc[2]}') 
print(f'Target location and station {least_distance_loc[2]} are ~{round(least_distance_loc[-1],1)}km apart')

quit()

# loop through JSON obj and print lat lon for each list in obj
# look at if statements to filter by state, perhaps also city (would require more data in core xls file)
for L in range(10000):
    # print(jobj['data'][0])
    try:
        print(jobj['data'][L])
        print(jobj['data'][L][0])
        print(jobj['data'][L][1])
        print(jobj['data'][L][2])
        print(jobj['data'][L][3])
        print(jobj['data'][L][4])
    except Exception as e:
        break
    

# Export Pandas DataFrame to JSON File
df.to_json(r'StationsDataTest.json',orient='split')


