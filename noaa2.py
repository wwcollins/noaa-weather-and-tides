    #noaa weather api collection
    #William Collins 2020, all rights reserved
    #noaa2.py:  a modification from noaa1.py returning targeted data per latlon

import requests
import json
import time
from datetime import datetime, timedelta
from pyld import jsonld
import socket
import os
from urllib.request import urlopen
import requests

print("Welcome to NOAA weather api collection. Alkemie Technologies LLC, William Collins 2020, All Rights Reserved")
time.sleep(3)


class noaa:
        
    def write2file(filename,attrib,content): #attrib is w or a.  w overwrites, a appends
        #f = open("demofile2.txt", "a")
        f = open(filename, attrib)
        f.write(content)
        f.close()
        
    def openfile(filename):
        #open and read the file
        f = open(filename, "r")
        print(f.read())

    def txt2jsonobj(json_string):
        json_obj = json.loads(json_string)
        return json_obj

    #DATA - from noaa1.py: Collect Information re. User IP addresses, location by IP, etc.
    print("-------------------ACQUIRING LOCAL USER DATA--------------------------------")

    #return state abbreviation 
    def get_us_state_abbrev(state):
        print(state)
        us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands':'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'Washington DC': 'DC',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
        }
        return us_state_abbrev [state]
        
    #test
    #print(get_us_state_abbrev('Texas'))


        
    """
    public_ip = requests.get("http://wtfismyip.com/text").text
    print(public_ip)
    ip2geotools 24.27.43.198 -d dbipcity -f json
    """

    # for user location, return hostname, localip, public_ip, state, state_abrev, geo_dict.  geo_dict leverages cmd line call from ip2geotools.  public ip from api: http://wtfismyip.com/text.  hostname and local IP from python socket lib.
    def getuser_location(): #pip install socket
        hostname = socket.gethostname()
        localip = socket.gethostbyname(hostname) 
        public_ip = requests.get('http://wtfismyip.com/text').text
        #ip2geotools 24.27.43.198 -d dbipcity -f json
        geoloc_cmd = 'ip2geotools ' + public_ip + ' -d dbipcity -f json'
        geoloc_cmd = geoloc_cmd.replace("\n","")
        #print (geoloc_cmd)
        geoloc = os.system(geoloc_cmd) #return success/fail code.  Fail !=0
        geoloc_out = os.popen(geoloc_cmd).read()  #dictionary returned from CMD execute
        print ("geoloc_out: " + geoloc_out)
        print(hostname + " " + str(localip) + " " + public_ip)
        #https://api.ipgeolocationapi.com/geolocate/91.213.103.0 #does not return state info
        #url = 'https://api.ipgeolocationapi.com/geolocate/' + public_ip
        #print (url)
        #r = requests.get(url)
        #print (r.text)
        #print(type(geoloc_out))
        geo_dict = json.loads(geoloc_out)
        #iterate through dictionary
        """ CMD and Output
        ip2geotools 24.27.43.198 -d dbipcity -f json
        {"ip_address": "24.27.43.198", "city": "Round Rock", "region": "Texas", "country": "US", "latitude": 30.508235, "longitude": -97.6788934}
        geoloc_out: {"ip_address": "24.27.43.198", "city": "Round Rock", "region": "Texas", "country": "US", "latitude": 30.508235, "longitude": -97.6788934}
        """
        for key, value in geo_dict.items(): 
            print(key, ":", value) 
        print(geo_dict['region'])
        state = geo_dict['region']
        state_abrev = self.get_us_state_abbrev(state)
        lat = geo_dict['latitude']
        lon = geo_dict['longitude']

        
        return hostname, localip, public_ip, state, state_abrev, geo_dict, lat, lon
        


    #Alerts:  https://api.weather.gov/alerts/active?area=TX  an alert for TX Extreme Weather
    print("-------------------ALERTS--------------------------------")

    def alerts(state):
        try:
            r = ""
            url = 'https://api.weather.gov/alerts/active?area=' + str(state)
            print (url)
            r = requests.get(url)
            print("requests status code=" + str(r.status_code))
            if r.status_code == 200:
                time.sleep(2)
                #print ("response=" + r.text)
                print("NOAA Alerts api success...")
                jsonobj = r.json()
                return r.text
            else:
                print("status=" + str(r.status_code))
                print("trying again..." + url)
                time.sleep(5)
                alerts(state)
        except Exception as e:
            print (e)
            return e


    print('*********************ALERTS INFORMATION********************')
    try:
        r_obj = txt2jsonobj(r) #returns JSON obj from text
    except Exception as e:
        print (e)
        
    try:
        title = r_obj['title']
        updated = r_obj['updated']
        areaDesc = r_obj['features'][0]['properties']['areaDesc']
        headline = r_obj['features'][0]['properties']['headline']
        description = r_obj['features'][0]['properties']['description']
        affectedZones = r_obj['features'][0]['properties']['affectedZones']

        print(title + " " + str(updated))
        print (areaDesc)
        print (headline)
        print (description)
        print ("affectedZones:")
        print (affectedZones)
    except Exception as e:
        print(e)
        

    print('*********************ALERTS INFORMATION - ITERATE****************')
    for n in range(100): 
        try:
            print("***************************** ID=" + str(n) + "***************************")
            areaDesc = r_obj['features'][n]['properties']['areaDesc']
            headline = r_obj['features'][n]['properties']['headline']
            description = r_obj['features'][n]['properties']['description']
            affectedZones = r_obj['features'][n]['properties']['affectedZones']
            print(title + " " + str(updated))
            print (areaDesc)
            print (headline)
            print (description)
            print ("affectedZones:" + str(affectedZones) + "\n")
        except Exception as e:
            print (e)
            break




    print("-------------------TIDES AND CURRRENTS --------------------------------")

    #TBD - implement - levarage with WeatherX.py with LCD output
    #https://tidesandcurrents.noaa.gov/api/#products
    #Water Temp
    #Example:  https://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20130808 15:00&end_date=20130808 15:06&station=8454000&product=water_temperature&units=english&time_zone=gmt&application=ports_screen&format=json
    #Example:  https://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20200725 15:00&end_date=20200808 15:06&station=8454000&product=water_temperature&units=english&time_zone=gmt&application=ports_screen&format=json
    #Tides - product = tide_predictions
    #https://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20200725%2015:00&end_date=20200725%2015:06&station=8775241&product=tide_prediction&format=json&units=english&time_zone=lst_ldt&datum=MLLW
    #8775241 - Aransas Pass TX
    #https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=8775241
    #https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20200701&end_date=20200731&datum=MLLW&station=8775241&time_zone=lst_ldt&units=english&interval=hilo&format=json

    #This is the format to use! Finally!!!
    #https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20200801&end_date=20200831&datum=MLLW&station=8775241&time_zone=lst_ldt&units=english&interval=hilo&format=json

    def tide_forecast(days_out):
        #https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20200801&end_date=20200831&datum=MLLW&station=8775241&time_zone=lst_ldt&units=english&interval=hilo&format=json
        
        now = datetime.now()
        begin_date = now.strftime('%Y%m%d')
        end_date = datetime.today() + timedelta(days_out)
        end_date = end_date.strftime('%Y%m%d')
        stationID = "8775241"
        print("start and end date")
        print(begin_date)
        print(end_date)
        url = "https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=" + begin_date + "&end_date=" + end_date + "&datum=MLLW&station=" + stationID + "&time_zone=lst_ldt&units=english&interval=hilo&format=json"
        print(url)
        try:
            r = ""
            print (url)
            r = requests.get(url)
            print("requests status code=" + str(r.status_code))
            if r.status_code == 200:
                time.sleep(2)
                #print ("response=" + r.text)
                print("NOAA Tide Data api success...")
                jsonobj = r.json()
                return r.text
            else:
                print("status=" + str(r.status_code))
                print("trying again..." + url)
                time.sleep(3)
        except Exception as e:
            print (e)
            return e
        
    #test
    days_out = 15
    r = tide_forecast(days_out)
    r_obj = txt2jsonobj(r) #returns JSON obj from text

    """
    print(r_obj['predictions'][0]['t'])
    print(r_obj['predictions'][0]['v'])
    print(r_obj['predictions'][0]['type'])
    """

    print('*********************TIDE INFORMATION - FORECAST****************')
    print()
    for n in range(0,100): 
        try:
            #print("***************************** ID=" + str(n) + "***************************")
            print()
            print(r_obj['predictions'][n]['t'] + " " + r_obj['predictions'][n]['type'] + " " + r_obj['predictions'][n]['v'])
            #print(r_obj['predictions'][n]['type'])
            #print(r_obj['predictions'][n]['v'])
            
        except Exception as e:
            #print (e)
            break


    """
    The CO-OPS API for data retrieval can be used to retrieve observations and predictions from CO-OPS stations.
    Station ID
    A 7 character station ID, or a currents station ID. Specify the station ID with the "station=" parameter.
    Example: station=9414290
    Station listings for various products can be viewed at https://tidesandcurrents.noaa.gov or viewed on a map at Tides & Currents Station Map
    Date & Time
    The API understands several parameters related to date ranges.
    All dates can be formatted as follows:
    yyyyMMdd, yyyyMMdd HH:mm, MM/dd/yyyy, or MM/dd/yyyy HH:mm
    """

    #Forecasts
    print("-------------------FORECASTS --------------------------------")
    """
    Forecasts are divided into 2.5km grids. Each NWS office is responsible for a section of the grid. The API endpoint for the forecast at a specific grid is:
    https://api.weather.gov/gridpoints/{office}/{grid X},{grid Y}/forecast
    For example: https://api.weather.gov/gridpoints/TOP/31,80/forecast

    If you do not know the grid that correlates to your location, you can use the /points endpoint to retrieve the exact grid endpoint by coordinates:
    https://api.weather.gov/points/{latitude},{longitude}
    For example: https://api.weather.gov/points/39.7456,-97.0892
    This will return the grid endpoint in the "forecast" property. Applications may cache the grid for a location to improve latency and reduce the additional lookup request. This endpoint also tells the application where to find information for issuing office, observation stations, and zones.
    """

    #Grid Coordinates - For example: https://api.weather.gov/points/39.7456,-97.0892

    def grid(lat,lon):
        try:
            url = "https://api.weather.gov/points/" + str(lat) + "," + str(lon)
            #print (url)
            r = requests.get(url)
            print (r.text)
            #jsonobj = r.json()
            return r.text
        except Exception as e:
            print (e)

 
    """
    # TBD pull office,grid_x,grid_y from JSON obj to use in api call below...
            "gridId": "EWX"
            "gridX": 157
            "gridY": 100
            "forecast": "https://api.weather.gov/gridpoints/EWX/157,100/forecast",
            "forecastHourly": "https://api.weather.gov/gridpoints/EWX/157,100/forecast/hourly",
            "forecastGridData": "https://api.weather.gov/gridpoints/EWX/157,100",
            "observationStations": "https://api.weather.gov/gridpoints/EWX/157,100/stations"
    """
    gridId = r_obj['properties']['gridId']
    gridX = r_obj['properties']['gridX']
    gridY = r_obj['properties']['gridY']
    forecast = r_obj['properties']['forecast']
    forecastHourly = r_obj['properties']['forecastHourly']
    forecastGridData = r_obj['properties']['forecastGridData']
    observationStations = r_obj['properties']['observationStations']
    print(gridId)
    print(gridX)
    print(gridY)
    print("forecast:" + forecast)
    print("forecastHourly:" + forecastHourly)
    print("forecastGridData:" + forecastGridData)
    print("observationStations:" + observationStations)

    filename = "noaa_weather__grid_" + str(lat) + " " + str(lon) + ".json"
    attrib = "w"
    content = r
    print(".....Writing Alert content to " + filename)
    write2file(filename,attrib,content)
    #openfile(filename)


    """
    https://api.weather.gov/points/{latitude},{longitude}
    For example: https://api.weather.gov/points/39.7456,-97.0892
    """

    print("-------------------POINTS INFORMATION--------------------------------")

    # Get /points information
    # e.g. https://api.weather.gov/points/39.7456,-97.0892

    def getpoints(lat,lon):
        url = "https://api.weather.gov/points/" + str(lat) + "," + str(lon)
        #print (url)
        r = requests.get(url)
        #print (r.text)
        #jsonobj = r.json()
        return r.text
        
    #test
    r = getpoints(lat,lon) #lat lon defined earlier in code

    filename = "noaa_weather_points_" + str(lat) + " " + str(lon) + ".json"
    attrib = "w"
    content = r
    print(".....Writing Points content to " + filename)
    write2file(filename,attrib,content)
    #openfile(filename)


    #quit()

    #Forecasts - Use Grid and Points Information to populate values: office, gridx, gridy"
    print("-------------------FORECASTS--------------------------------")

    """
    Forecasts are divided into 2.5km grids. Each NWS office is responsible for a section of the grid. The API endpoint for the forecast at a specific grid is:

    https://api.weather.gov/gridpoints/{office}/{grid X},{grid Y}/forecast
    For example: https://api.weather.gov/gridpoints/TOP/31,80/forecast
    If you do not know the grid that correlates to your location, you can use the /points endpoint to retrieve the exact grid
    endpoint by coordinates:
    https://api.weather.gov/points/{latitude},{longitude}
    For example: https://api.weather.gov/points/39.7456,-97.0892
    """

    #https://api.weather.gov/gridpoints/{office}/{grid X},{grid Y}/forecast
    #example: https://api.weather.gov/gridpoints/TOP/31,80/forecast
    def forecast(office,gridX,gridY):
        try:
            url = "https://api.weather.gov/gridpoints/" + office + "/" + str(gridX)  + "," + str(gridY) + "/forecast"  # TBD get 
            #url = "https://api.weather.gov/gridpoints/TOP/31,80/forecast"
            #print (url)
            r = requests.get(url)
            print("requests status code=" + str(r.status_code))
            if r.status_code == 200:
                time.sleep(2)
                #print ("response=" + r.text)
                print("NOAA Forecast api success...")
                jsonobj = r.json()
                return r.text
            else:
                print("status=" + str(r.status_code))
                print("trying again..." + url)
                time.sleep(5)
                forecast(office,gridX,gridY)
        except Exception as e:
            #print (e)
            forecast(office,gridX,gridY)
            
    #office = 'TOP' #Need to retrieve this from previous api call
    #grid_x = "31" #Need to retrieve this from previous api call
    #grid_y = "80" #Need to retrieve this from previous api call

    office = gridId
    r = forecast(office,gridX,gridY)
    #print(r)

    r_obj = txt2jsonobj(r) #returns JSON obj from text
    #print(r_obj)

    """
    "name": "This Afternoon",
    "startTime": "2020-08-04T17:00:00-05:00",
    "endTime": "2020-08-04T18:00:00-05:00",
    "isDaytime": true,
    "temperature": 98,
    "temperatureUnit": "F",
    "temperatureTrend": null,
    "windSpeed": "5 mph",
    "windDirection": "S",
    "icon": "https://api.weather.gov/icons/land/day/tsra_hi?size=medium",
    "shortForecast": "Slight Chance Showers And Thunderstorms",
    "detailedForecast": "A slight chance of showers and thunderstorms. Mostly sunny, with a high near 98. Heat index values as high as 100. South wind around 5 mph."
    """

    """
    name = r_obj['properties']['periods'][0]['name']
    temperature = r_obj['properties']['periods'][0]['temperature']
    temperatureUnit = r_obj['properties']['periods'][0]['temperatureUnit']
    temp = "Temperature: " + str(temperature) + temperatureUnit
    windSpeed = r_obj['properties']['periods'][0]['windSpeed']
    windDirection = r_obj['properties']['periods'][0]['windDirection']
    wind = "Wind: " + str(windSpeed) + " out of the " + windDirection
    shortForecast = r_obj['properties']['periods'][0]['shortForecast']
    detailedForecast = r_obj['properties']['periods'][0]['detailedForecast']

    print (name)
    print(temp)
    print(wind)
    print(shortForecast)
    print(detailedForecast)
    """

    #quit()

    print('*********************FORECAST INFORMATION - ITERATE****************')
    for n in range(0,100): 
        try:
            #print("***************************** ID=" + str(n) + "***************************")
            print()
            name = r_obj['properties']['periods'][n]['name']
            temperature = r_obj['properties']['periods'][n]['temperature']
            temperatureUnit = r_obj['properties']['periods'][n]['temperatureUnit']
            temp = str(temperature) + temperatureUnit
            windSpeed = r_obj['properties']['periods'][n]['windSpeed']
            windDirection = r_obj['properties']['periods'][n]['windDirection']
            wind = "Wind: " + str(windSpeed) + " out of the " + windDirection
            shortForecast = r_obj['properties']['periods'][n]['shortForecast']
            detailedForecast = r_obj['properties']['periods'][n]['detailedForecast']        
            startTime = r_obj['properties']['periods'][n]['startTime']
            
            print (name + " at " + startTime + ":")
            print(detailedForecast)
            fullForecast = "For " + name + " the temperature will be " + temp + ".  The wind will be " + windSpeed + " coming from the " + windDirection
            print("More: " + fullForecast)
            #print(temp)
            #print(wind)
            #print(shortForecast)
            
        except Exception as e:
            #print (e)
            break

    filename = "noaa_weather_forecast_" + str(lat) + " " + str(lon) + ".json"
    attrib = "w"
    content = r
    print(".....Writing Forecast content to " + filename)
    write2file(filename,attrib,content)
    #openfile(filename)
    
# end class noaa()
    
objNOAA = noaa()
hostname, localip, public_ip, state, state_abrev, geo_dict, lat, lon = objNOAA.getuser_location()
#testget_host_ip = getuser_location() 
#print(testget_host_ip)
state = objNOAA.get_us_state_abbrev(geo_dict['region']) #return 2 letter abbrev for state
lat = geo_dict['latitude']
lon = geo_dict['longitude']
latlon = str(lat) + "," + str(lon)
print ("latitude, longitude:", latlon)
#test above
#state = "tx" #use state per def return above - TBD add exception and null string handling
r = objNOAA.alerts(state)  #get NOAA weather alerts by state
#print (r)
#print(type(r))

filename = "noaa_weather_alerts_" + state + ".json"

attrib = "w"
content = r
print(".....Writing Alert content to " + filename)
try:
    write2file(filename,attrib,content)
    #openfile(filename)
except Exception as e:
    print(e)
    
filename = "noaa_weather__tides_forecast_" + str(lat) + ".json"
attrib = "w"
content = r
print(".....Writing Alert content to " + filename)
write2file(filename,attrib,content)
#openfile(filename)

#test above
lat = '39.7456'
lon = '-97.0892'
r = grid(lat,lon) #variables now defined via functions above
#print (r)
r_obj = txt2jsonobj(r) #returns JSON obj from text

print("********************************* GRID INFORMATION " + str(lat) + " " + str(lon) + " *******************************")
    



    
    

"""
    json output examples

    mage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. Flood control\nsystems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- https://www.weather.gov/srh/tropical?office=crp",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KCRP.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "CRPTCVCRP"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348470-3639019",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.4569999,
                                28.16
                            ],
                            [
                                -97.450000000000003,
                                28.148
                            ],
                            [
                                -97.442999999999998,
                                28.154
                            ],
                            [
                                -97.447000000000003,
                                28.137
                            ],
                            [
                                -97.442999999999998,
                                28.132000000000001
                            ],
                            [
                                -97.438999899999999,
                                28.138000000000002
                            ],
                            [
                                -97.423000000000002,
                                28.142000000000003
                            ],
                            [
                                -97.433999999999997,
                                28.129000000000001
                            ],
                            [
                                -97.427999999999997,
                                28.127000000000002
                            ],
                            [
                                -97.426000000000002,
                                28.117000000000001
                            ],
                            [
                                -97.417000000000002,
                                28.122
                            ],
                            [
                                -97.405000000000001,
                                28.119
                            ],
                            [
                                -97.405000000000001,
                                28.108999999999998
                            ],
                            [
                                -97.400000000000006,
                                28.119999999999997
                            ],
                            [
                                -97.405000000000001,
                                28.122999999999998
                            ],
                            [
                                -97.403999999999996,
                                28.128999999999998
                            ],
                            [
                                -97.382999999999996,
                                28.124999999999996
                            ],
                            [
                                -97.378,
                                28.138999999999996
                            ],
                            [
                                -97.346000000000004,
                                28.118999999999996
                            ],
                            [
                                -97.340000000000003,
                                28.131999999999998
                            ],
                            [
                                -97.325999899999999,
                                28.126999999999999
                            ],
                            [
                                -97.329999999999998,
                                28.119999999999997
                            ],
                            [
                                -97.325000000000003,
                                28.119999999999997
                            ],
                            [
                                -97.317999999999998,
                                28.131999999999998
                            ],
                            [
                                -97.326999999999998,
                                28.132999999999999
                            ],
                            [
                                -97.316999899999999,
                                28.137
                            ],
                            [
                                -97.308999999999997,
                                28.119
                            ],
                            [
                                -97.316999899999999,
                                28.109999999999999
                            ],
                            [
                                -97.301999999999992,
                                28.103999999999999
                            ],
                            [
                                -97.289999999999992,
                                28.114999999999998
                            ],
                            [
                                -97.282999999999987,
                                28.091999999999999
                            ],
                            [
                                -97.34899999999999,
                                27.984999999999999
                            ],
                            [
                                -97.405999999999992,
                                27.875
                            ],
                            [
                                -97.446999999999989,
                                27.867000000000001
                            ],
                            [
                                -97.459999899999985,
                                27.862000000000002
                            ],
                            [
                                -97.470999999999989,
                                27.863000000000003
                            ],
                            [
                                -97.480999999999995,
                                27.860000000000003
                            ],
                            [
                                -97.492999999999995,
                                27.884000000000004
                            ],
                            [
                                -97.527000000000001,
                                27.870000000000005
                            ],
                            [
                                -97.498000000000005,
                                27.851000000000006
                            ],
                            [
                                -97.488,
                                27.844000000000005
                            ],
                            [
                                -97.501000000000005,
                                27.847000000000005
                            ],
                            [
                                -97.536000000000001,
                                27.848000000000006
                            ],
                            [
                                -97.542000000000002,
                                27.858000000000008
                            ],
                            [
                                -97.555999999999997,
                                27.861000000000008
                            ],
                            [
                                -97.591999999999999,
                                27.857000000000006
                            ],
                            [
                                -97.608999999999995,
                                27.872000000000007
                            ],
                            [
                                -97.609999999999999,
                                27.890000000000008
                            ],
                            [
                                -97.626999999999995,
                                27.895000000000007
                            ],
                            [
                                -97.631999999999991,
                                27.893000000000008
                            ],
                            [
                                -97.626999999999995,
                                27.876000000000008
                            ],
                            [
                                -97.638999999999996,
                                27.866000000000007
                            ],
                            [
                                -97.643000000000001,
                                27.872000000000007
                            ],
                            [
                                -97.674999999999997,
                                27.883000000000006
                            ],
                            [
                                -97.670999999999992,
                                27.892000000000007
                            ],
                            [
                                -97.681999999999988,
                                27.902000000000008
                            ],
                            [
                                -97.688999899999985,
                                27.900000000000009
                            ],
                            [
                                -97.690999999999988,
                                27.917000000000009
                            ],
                            [
                                -97.707999999999984,
                                27.923000000000009
                            ],
                            [
                                -97.715999899999986,
                                27.91800000000001
                            ],
                            [
                                -97.715999899999986,
                                27.91200000000001
                            ],
                            [
                                -97.72499999999998,
                                27.916000000000011
                            ],
                            [
                                -97.735999999999976,
                                27.91200000000001
                            ],
                            [
                                -97.729999999999976,
                                27.923000000000009
                            ],
                            [
                                -97.745999999999981,
                                27.92700000000001
                            ],
                            [
                                -97.748999999999981,
                                27.93300000000001
                            ],
                            [
                                -97.760999999999981,
                                27.923000000000009
                            ],
                            [
                                -97.765999999999977,
                                27.92700000000001
                            ],
                            [
                                -97.763999999999982,
                                27.938000000000009
                            ],
                            [
                                -97.775999999999982,
                                27.938000000000009
                            ],
                            [
                                -97.779999999999987,
                                27.945000000000011
                            ],
                            [
                                -97.775999999999982,
                                27.948000000000011
                            ],
                            [
                                -97.794999999999987,
                                27.943000000000012
                            ],
                            [
                                -97.796999999999983,
                                27.934000000000012
                            ],
                            [
                                -97.805999999999983,
                                27.935000000000013
                            ],
                            [
                                -97.816999899999985,
                                27.970000000000013
                            ],
                            [
                                -97.806999999999988,
                                27.973000000000013
                            ],
                            [
                                -97.798999999999992,
                                27.996000000000013
                            ],
                            [
                                -97.806999999999988,
                                27.989000000000011
                            ],
                            [
                                -97.793999999999983,
                                28.027000000000012
                            ],
                            [
                                -97.805999999999983,
                                28.041000000000011
                            ],
                            [
                                -97.85299999999998,
                                28.03700000000001
                            ],
                            [
                                -97.877999999999986,
                                28.047000000000011
                            ],
                            [
                                -97.874999999999986,
                                28.050000000000011
                            ],
                            [
                                -97.883999999999986,
                                28.056000000000012
                            ],
                            [
                                -97.899999999999991,
                                28.066000000000013
                            ],
                            [
                                -97.897999999999996,
                                28.079000000000015
                            ],
                            [
                                -97.908000000000001,
                                28.089000000000016
                            ],
                            [
                                -97.906999999999996,
                                28.097000000000016
                            ],
                            [
                                -97.896999999999991,
                                28.101000000000017
                            ],
                            [
                                -97.902999999999992,
                                28.114000000000019
                            ],
                            [
                                -97.816999899999985,
                                28.177000000000017
                            ],
                            [
                                -97.567999999999984,
                                28.130000000000017
                            ],
                            [
                                -97.540999999999983,
                                28.165000000000017
                            ],
                            [
                                -97.520999999999987,
                                28.152000000000015
                            ],
                            [
                                -97.481999999999985,
                                28.169000000000015
                            ],
                            [
                                -97.475999999999985,
                                28.179000000000016
                            ],
                            [
                                -97.47199999999998,
                                28.155000000000015
                            ],
                            [
                                -97.4569999,
                                28.16
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348470-3639019",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348470-3639019",
                    "areaDesc": "Inland San Patricio",
                    "geocode": {
                        "UGC": [
                            "TXZ244"
                        ],
                        "SAME": [
                            "048409"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ244"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348038-3638735",
                            "identifier": "NWS-IDP-PROD-4348038-3638735",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T18:19:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347734-3638525",
                            "identifier": "NWS-IDP-PROD-4347734-3638525",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:04:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347734-3638524",
                            "identifier": "NWS-IDP-PROD-4347734-3638524",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:04:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T22:00:00-05:00",
                    "effective": "2020-07-24T22:00:00-05:00",
                    "onset": "2020-07-24T22:00:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Extreme",
                    "certainty": "Likely",
                    "urgency": "Immediate",
                    "event": "Hurricane Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Corpus Christi TX",
                    "headline": "Hurricane Warning issued July 24 at 10:00PM CDT by NWS Corpus Christi TX",
                    "description": "* LOCATIONS AFFECTED\n- Mathis\n- Sinton\n- Taft\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 30-40 mph with gusts to 50 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for 1-3 feet\nabove ground somewhere within surge prone areas\n- Window of concern: Saturday afternoon until Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has increased from the previous\nassessment.\n- PLAN: There is little to no threat of storm surge flooding.\nRough surf, coastal erosion, and life-threatening rip\ncurrents are possible.\n- PREPARE: Little to no preparations for storm surge flooding\nare needed.\n- ACT: Follow the instructions of local officials. Monitor\nforecasts.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional surge impacts expected. Community\nofficials are now assessing the extent of actual surge\nimpacts accordingly.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. Flood control\nsystems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- https://www.weather.gov/srh/tropical?office=crp",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "HURRICANE WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KCRP.HU.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "CRPTCVCRP"
                        ],
                        "BLOCKCHANNEL": [
                            "EAS",
                            "NWEM",
                            "CMAS"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348471-3639020",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.884,
                                28.056000000000001
                            ],
                            [
                                -97.875,
                                28.050000000000001
                            ],
                            [
                                -97.878,
                                28.047000000000001
                            ],
                            [
                                -97.852999999999994,
                                28.036999999999999
                            ],
                            [
                                -97.805999999999997,
                                28.041
                            ],
                            [
                                -97.793999999999997,
                                28.027000000000001
                            ],
                            [
                                -97.807000000000002,
                                27.989000000000001
                            ],
                            [
                                -97.933999999999997,
                                27.885000000000002
                            ],
                            [
                                -97.933999999999997,
                                27.777000000000001
                            ],
                            [
                                -97.941999899999999,
                                27.636000000000003
                            ],
                            [
                                -98.058999999999997,
                                27.636000000000003
                            ],
                            [
                                -98.057999999999993,
                                27.261000000000003
                            ],
                            [
                                -98.231999999999999,
                                27.263000000000002
                            ],
                            [
                                -98.234999999999999,
                                28.058000000000003
                            ],
                            [
                                -97.884,
                                28.056000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348471-3639020",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348471-3639020",
                    "areaDesc": "Jim Wells",
                    "geocode": {
                        "UGC": [
                            "TXZ241"
                        ],
                        "SAME": [
                            "048249"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ241"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348043-3638742",
                            "identifier": "NWS-IDP-PROD-4348043-3638742",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T18:19:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347728-3638511",
                            "identifier": "NWS-IDP-PROD-4347728-3638511",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:04:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347728-3638510",
                            "identifier": "NWS-IDP-PROD-4347728-3638510",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:04:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T22:00:00-05:00",
                    "effective": "2020-07-24T22:00:00-05:00",
                    "onset": "2020-07-24T22:00:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Extreme",
                    "certainty": "Likely",
                    "urgency": "Immediate",
                    "event": "Hurricane Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Corpus Christi TX",
                    "headline": "Hurricane Warning issued July 24 at 10:00PM CDT by NWS Corpus Christi TX",
                    "description": "* LOCATIONS AFFECTED\n- Alice\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 35-45 mph with gusts to 60 mph\n- Window for Tropical Storm force winds: early Saturday\nafternoon until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 58\nto 73 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for dangerous wind of equivalent strong tropical\nstorm force.\n- PREPARE: Remaining efforts to protect life and property\nshould be completed as soon as possible. Prepare for\nsignificant wind damage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Significant\n- Some damage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. Flood control\nsystems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- https://www.weather.gov/srh/tropical?office=crp",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "HURRICANE WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KCRP.HU.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "CRPTCVCRP"
                        ],
                        "BLOCKCHANNEL": [
                            "EAS",
                            "NWEM",
                            "CMAS"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348468-3639017",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.829999999999998,
                                28.677
                            ],
                            [
                                -97.823999999999998,
                                28.670999999999999
                            ],
                            [
                                -97.792000000000002,
                                28.677
                            ],
                            [
                                -97.775999999999996,
                                28.669
                            ],
                            [
                                -97.756,
                                28.655000000000001
                            ],
                            [
                                -97.751999999999995,
                                28.641000000000002
                            ],
                            [
                                -97.730999999999995,
                                28.626000000000001
                            ],
                            [
                                -97.695999999999998,
                                28.542000000000002
                            ],
                            [
                                -97.668999999999997,
                                28.535
                            ],
                            [
                                -97.644999999999996,
                                28.521000000000001
                            ],
                            [
                                -97.62299999999999,
                                28.529
                            ],
                            [
                                -97.562999999999988,
                                28.515999999999998
                            ],
                            [
                                -97.553999999999988,
                                28.501999999999999
                            ],
                            [
                                -97.549999999999983,
                                28.451000000000001
                            ],
                            [
                                -97.520999999999987,
                                28.446000000000002
                            ],
                            [
                                -97.523999999999987,
                                28.441000000000003
                            ],
                            [
                                -97.516999999999982,
                                28.432000000000002
                            ],
                            [
                                -97.497999999999976,
                                28.438000000000002
                            ],
                            [
                                -97.481999999999971,
                                28.435000000000002
                            ],
                            [
                                -97.46099999999997,
                                28.408000000000001
                            ],
                            [
                                -97.450999899999971,
                                28.409000000000002
                            ],
                            [
                                -97.44599999999997,
                                28.404000000000003
                            ],
                            [
                                -97.427999999999969,
                                28.413000000000004
                            ],
                            [
                                -97.420999999999964,
                                28.405000000000005
                            ],
                            [
                                -97.397999999999968,
                                28.403000000000006
                            ],
                            [
                                -97.400999999999968,
                                28.394000000000005
                            ],
                            [
                                -97.390999999999963,
                                28.397000000000006
                            ],
                            [
                                -97.384999999999962,
                                28.390000000000004
                            ],
                            [
                                -97.375999999999962,
                                28.389000000000003
                            ],
                            [
                                -97.540999999999968,
                                28.165000000000003
                            ],
                            [
                                -97.567999999999969,
                                28.130000000000003
                            ],
                            [
                                -97.816999899999971,
                                28.177000000000003
                            ],
                            [
                                -97.808999999999969,
                                28.185000000000002
                            ],
                            [
                                -98.089999999999975,
                                28.663000000000004
                            ],
                            [
                                -98.005999999999972,
                                28.691000000000003
                            ],
                            [
                                -97.914999999999978,
                                28.719000000000001
                            ],
                            [
                                -97.892999999999972,
                                28.700000000000003
                            ],
                            [
                                -97.829999999999998,
                                28.677
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348468-3639017",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348468-3639017",
                    "areaDesc": "Bee",
                    "geocode": {
                        "UGC": [
                            "TXZ232"
                        ],
                        "SAME": [
                            "048025"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ232"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345603-3637206",
                            "identifier": "NWS-IDP-PROD-4345603-3637206",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T15:55:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345603-3637205",
                            "identifier": "NWS-IDP-PROD-4345603-3637205",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T15:55:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346544-3637796",
                            "identifier": "NWS-IDP-PROD-4346544-3637796",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346918-3638042",
                            "identifier": "NWS-IDP-PROD-4346918-3638042",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T04:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348037-3638734",
                            "identifier": "NWS-IDP-PROD-4348037-3638734",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T18:19:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347216-3638220",
                            "identifier": "NWS-IDP-PROD-4347216-3638220",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:25:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347720-3638496",
                            "identifier": "NWS-IDP-PROD-4347720-3638496",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:04:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T22:00:00-05:00",
                    "effective": "2020-07-24T22:00:00-05:00",
                    "onset": "2020-07-24T22:00:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Corpus Christi TX",
                    "headline": "Tropical Storm Warning issued July 24 at 10:00PM CDT by NWS Corpus Christi TX",
                    "description": "* LOCATIONS AFFECTED\n- Beeville\n\n* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 20-30 mph with gusts to 40 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, arroyos, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- https://www.weather.gov/srh/tropical?office=crp",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KCRP.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "CRPTCVCRP"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348473-3639022",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.082999999999998,
                                28.533999999999999
                            ],
                            [
                                -97.078999899999999,
                                28.544999999999998
                            ],
                            [
                                -97.058999999999997,
                                28.542999999999999
                            ],
                            [
                                -97.055999999999997,
                                28.550000000000001
                            ],
                            [
                                -97.045999999999992,
                                28.548999999999999
                            ],
                            [
                                -97.049999999999997,
                                28.535999999999998
                            ],
                            [
                                -97.042000000000002,
                                28.531999999999996
                            ],
                            [
                                -97.031000000000006,
                                28.540999999999997
                            ],
                            [
                                -97.025000000000006,
                                28.538999999999998
                            ],
                            [
                                -97.021000000000001,
                                28.516999999999999
                            ],
                            [
                                -96.989000000000004,
                                28.501999999999999
                            ],
                            [
                                -96.956000000000003,
                                28.503999999999998
                            ],
                            [
                                -96.920000000000002,
                                28.486999999999998
                            ],
                            [
                                -96.911000000000001,
                                28.488999999999997
                            ],
                            [
                                -96.915999999999997,
                                28.497999999999998
                            ],
                            [
                                -96.906999999999996,
                                28.505999999999997
                            ],
                            [
                                -96.890999999999991,
                                28.507999999999996
                            ],
                            [
                                -96.864999999999995,
                                28.490999999999996
                            ],
                            [
                                -96.86099999999999,
                                28.475999999999996
                            ],
                            [
                                -96.84899999999999,
                                28.475999999999996
                            ],
                            [
                                -96.838999999999984,
                                28.456999999999997
                            ],
                            [
                                -96.824999999999989,
                                28.446999999999996
                            ],
                            [
                                -96.892999999999986,
                                28.417999999999996
                            ],
                            [
                                -97.10799999999999,
                                28.291999999999994
                            ],
                            [
                                -97.123999999999995,
                                28.272999999999996
                            ],
                            [
                                -97.283000000000001,
                                28.091999999999995
                            ],
                            [
                                -97.290000000000006,
                                28.114999999999995
                            ],
                            [
                                -97.302000000000007,
                                28.103999999999996
                            ],
                            [
                                -97.316999900000013,
                                28.109999999999996
                            ],
                            [
                                -97.309000000000012,
                                28.118999999999996
                            ],
                            [
                                -97.316999900000013,
                                28.136999999999997
                            ],
                            [
                                -97.327000000000012,
                                28.132999999999996
                            ],
                            [
                                -97.318000000000012,
                                28.131999999999994
                            ],
                            [
                                -97.325000000000017,
                                28.119999999999994
                            ],
                            [
                                -97.330000000000013,
                                28.119999999999994
                            ],
                            [
                                -97.325999900000014,
                                28.126999999999995
                            ],
                            [
                                -97.340000000000018,
                                28.131999999999994
                            ],
                            [
                                -97.346000000000018,
                                28.118999999999993
                            ],
                            [
                                -97.378000000000014,
                                28.138999999999992
                            ],
                            [
                                -97.38300000000001,
                                28.124999999999993
                            ],
                            [
                                -97.404000000000011,
                                28.128999999999994
                            ],
                            [
                                -97.405000000000015,
                                28.122999999999994
                            ],
                            [
                                -97.40000000000002,
                                28.119999999999994
                            ],
                            [
                                -97.405000000000015,
                                28.108999999999995
                            ],
                            [
                                -97.405000000000015,
                                28.118999999999996
                            ],
                            [
                                -97.417000000000016,
                                28.121999999999996
                            ],
                            [
                                -97.426000000000016,
                                28.116999999999997
                            ],
                            [
                                -97.428000000000011,
                                28.126999999999999
                            ],
                            [
                                -97.434000000000012,
                                28.128999999999998
                            ],
                            [
                                -97.423000000000016,
                                28.141999999999999
                            ],
                            [
                                -97.438999900000013,
                                28.137999999999998
                            ],
                            [
                                -97.443000000000012,
                                28.131999999999998
                            ],
                            [
                                -97.447000000000017,
                                28.136999999999997
                            ],
                            [
                                -97.443000000000012,
                                28.153999999999996
                            ],
                            [
                                -97.450000000000017,
                                28.147999999999996
                            ],
                            [
                                -97.456999900000014,
                                28.159999999999997
                            ],
                            [
                                -97.472000000000008,
                                28.154999999999998
                            ],
                            [
                                -97.476000000000013,
                                28.178999999999998
                            ],
                            [
                                -97.482000000000014,
                                28.168999999999997
                            ],
                            [
                                -97.521000000000015,
                                28.151999999999997
                            ],
                            [
                                -97.541000000000011,
                                28.164999999999999
                            ],
                            [
                                -97.376000000000005,
                                28.388999999999999
                            ],
                            [
                                -97.161000000000001,
                                28.553000000000001
                            ],
                            [
                                -97.143000000000001,
                                28.548999999999999
                            ],
                            [
                                -97.138999999999996,
                                28.553999999999998
                            ],
                            [
                                -97.128,
                                28.545999999999999
                            ],
                            [
                                -97.103999999999999,
                                28.553999999999998
                            ],
                            [
                                -97.082999999999998,
                                28.533999999999999
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348473-3639022",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348473-3639022",
                    "areaDesc": "Inland Refugio",
                    "geocode": {
                        "UGC": [
                            "TXZ246"
                        ],
                        "SAME": [
                            "048391"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ246"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346920-3638044",
                            "identifier": "NWS-IDP-PROD-4346920-3638044",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T04:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348031-3638725",
                            "identifier": "NWS-IDP-PROD-4348031-3638725",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T18:19:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347213-3638217",
                            "identifier": "NWS-IDP-PROD-4347213-3638217",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:25:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347727-3638509",
                            "identifier": "NWS-IDP-PROD-4347727-3638509",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:04:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345596-3637192",
                            "identifier": "NWS-IDP-PROD-4345596-3637192",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T15:55:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345596-3637191",
                            "identifier": "NWS-IDP-PROD-4345596-3637191",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T15:55:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346527-3637779",
                            "identifier": "NWS-IDP-PROD-4346527-3637779",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:01:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T22:00:00-05:00",
                    "effective": "2020-07-24T22:00:00-05:00",
                    "onset": "2020-07-24T22:00:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Corpus Christi TX",
                    "headline": "Tropical Storm Warning issued July 24 at 10:00PM CDT by NWS Corpus Christi TX",
                    "description": "* LOCATIONS AFFECTED\n- Refugio\n- Woodsboro\n\n* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 20-30 mph with gusts to 40 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for 1-3 feet\nabove ground somewhere within surge prone areas\n- Window of concern: Saturday afternoon until Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Shelter against storm surge flooding greater than 1\nfoot above ground.\n- PREPARE: All flood preparations should be complete. Expect\nflooding of low-lying roads and property.\n- ACT: Stay away from storm surge prone areas. Continue to\nfollow the instructions of local officials.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, arroyos, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- https://www.weather.gov/srh/tropical?office=crp",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KCRP.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "CRPTCVCRP"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348465-3639013",
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [
                                    -97.123999999999995,
                                    28.273
                                ],
                                [
                                    -97.11699999999999,
                                    28.259999999999998
                                ],
                                [
                                    -97.125999999999991,
                                    28.253999999999998
                                ],
                                [
                                    -97.097999999999985,
                                    28.231999999999999
                                ],
                                [
                                    -97.10199999999999,
                                    28.227
                                ],
                                [
                                    -97.074999999999989,
                                    28.219000000000001
                                ],
                                [
                                    -97.054999999999993,
                                    28.204000000000001
                                ],
                                [
                                    -97.039999999999992,
                                    28.207000000000001
                                ],
                                [
                                    -97.038999999999987,
                                    28.205000000000002
                                ],
                                [
                                    -97.035999999999987,
                                    28.201000000000001
                                ],
                                [
                                    -97.017999999999986,
                                    28.202000000000002
                                ],
                                [
                                    -97.030999999999992,
                                    28.189
                                ],
                                [
                                    -97.103999999999985,
                                    28.161000000000001
                                ],
                                [
                                    -97.112999999999985,
                                    28.156000000000002
                                ],
                                [
                                    -97.129999999999981,
                                    28.145000000000003
                                ],
                                [
                                    -97.208999999999975,
                                    28.096000000000004
                                ],
                                [
                                    -97.22199999999998,
                                    28.076000000000004
                                ],
                                [
                                    -97.234999999999985,
                                    28.063000000000002
                                ],
                                [
                                    -97.246999999999986,
                                    28.070000000000004
                                ],
                                [
                                    -97.261999999999986,
                                    28.078000000000003
                                ],
                                [
                                    -97.261999999999986,
                                    28.088000000000005
                                ],
                                [
                                    -97.282999999999987,
                                    28.092000000000006
                                ],
                                [
                                    -97.123999999999995,
                                    28.273
                                ]
                            ]
                        ],
                        [
                            [
                                [
                                    -97.123999999999981,
                                    28.273000000000007
                                ],
                                [
                                    -97.107999999999976,
                                    28.292000000000005
                                ],
                                [
                                    -96.892999999999972,
                                    28.418000000000006
                                ],
                                [
                                    -96.824999999999974,
                                    28.447000000000006
                                ],
                                [
                                    -96.810999999999979,
                                    28.431000000000008
                                ],
                                [
                                    -96.784999999999982,
                                    28.448000000000008
                                ],
                                [
                                    -96.779999999999987,
                                    28.442000000000007
                                ],
                                [
                                    -96.771999999999991,
                                    28.429000000000006
                                ],
                                [
                                    -96.762999999999991,
                                    28.426000000000005
                                ],
                                [
                                    -96.763999999999996,
                                    28.412000000000006
                                ],
                                [
                                    -96.778999999999996,
                                    28.400000000000006
                                ],
                                [
                                    -96.8379999,
                                    28.433000000000007
                                ],
                                [
                                    -96.859999999999999,
                                    28.414000000000009
                                ],
                                [
                                    -96.828999899999999,
                                    28.381000000000007
                                ],
                                [
                                    -96.795000000000002,
                                    28.364000000000008
                                ],
                                [
                                    -96.790000000000006,
                                    28.319000000000006
                                ],
                                [
                                    -97.123999999999981,
                                    28.273000000000007
                                ]
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348465-3639013",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348465-3639013",
                    "areaDesc": "Coastal Refugio",
                    "geocode": {
                        "UGC": [
                            "TXZ346"
                        ],
                        "SAME": [
                            "048391"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ346"
                    ],
                    "references": [],
                    "sent": "2020-07-24T22:00:00-05:00",
                    "effective": "2020-07-24T22:00:00-05:00",
                    "onset": "2020-07-24T22:00:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Extreme",
                    "certainty": "Likely",
                    "urgency": "Immediate",
                    "event": "Hurricane Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Corpus Christi TX",
                    "headline": "Hurricane Warning issued July 24 at 10:00PM CDT by NWS Corpus Christi TX",
                    "description": "A Hurricane Warning means hurricane-force winds are expected\nsomewhere within this area within the next 36 hours\n\n* LOCATIONS AFFECTED\n- Bayside\n- Austwell\n\n* WIND\n- LATEST LOCAL FORECAST: Tropical storm force winds remain\npossible\n- Peak Wind Forecast: 25-35 mph with gusts to 45 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Life-threatening storm surge possible\n- Peak Storm Surge Inundation: The potential for 2-4 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday afternoon\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 3 feet above ground\n- The storm surge threat has increased from the previous\nassessment.\n- PLAN: Shelter against life-threatening storm surge of\ngreater than 3 feet above ground.\n- PREPARE: Flood preparations and ordered evacuations should\nbe complete. Evacuees should be in shelters well away from\nstorm surge flooding.\n- ACT: Remain sheltered in a safe location. Do not venture\noutside.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. Flood control\nsystems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- https://www.weather.gov/srh/tropical?office=crp",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "HURRICANE WARNING IN EFFECT... ...STORM SURGE WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.EXA.KCRP.HU.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "CRPTCVCRP"
                        ],
                        "BLOCKCHANNEL": [
                            "EAS",
                            "NWEM"
                        ],
                        "WEAHandling": [
                            "Imminent Threat"
                        ],
                        "CMAMlongtext": [
                            "National Weather Service: A HURRICANE WARNING is in effect for this area for dangerous and damaging winds. This warning is issued up to 36 hours before hazardous conditions begin. Urgently complete efforts to protect life and property. Have food, water, cash, fuel, and medications for 3+ days. FOLLOW INSTRUCTIONS FROM LOCAL OFFICIALS."
                        ],
                        "CMAMtext": [
                            "NWS: HURRICANE WARNING this area. Check media and local authorities."
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348432-3638974",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -98.231999999999999,
                                27.263000000000002
                            ],
                            [
                                -98.057999999999993,
                                27.261000000000003
                            ],
                            [
                                -97.98599999999999,
                                27.261000000000003
                            ],
                            [
                                -97.984999999999985,
                                27.209000000000003
                            ],
                            [
                                -97.984999999999985,
                                26.781000000000002
                            ],
                            [
                                -98.320999999999984,
                                26.783000000000001
                            ],
                            [
                                -98.422999999999988,
                                26.784000000000002
                            ],
                            [
                                -98.417999999999992,
                                27.055000000000003
                            ],
                            [
                                -98.465999899999986,
                                27.055000000000003
                            ],
                            [
                                -98.466999999999985,
                                27.141000000000002
                            ],
                            [
                                -98.492999999999981,
                                27.142000000000003
                            ],
                            [
                                -98.492999999999981,
                                27.235000000000003
                            ],
                            [
                                -98.506999999999977,
                                27.240000000000002
                            ],
                            [
                                -98.511999999999972,
                                27.251000000000001
                            ],
                            [
                                -98.530999999999977,
                                27.255000000000003
                            ],
                            [
                                -98.535999999999973,
                                27.264000000000003
                            ],
                            [
                                -98.523999999999972,
                                27.265000000000004
                            ],
                            [
                                -98.231999999999999,
                                27.263000000000002
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348432-3638974",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348432-3638974",
                    "areaDesc": "Brooks",
                    "geocode": {
                        "UGC": [
                            "TXZ250"
                        ],
                        "SAME": [
                            "048047"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ250"
                    ],
                    "references": [],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Extreme",
                    "certainty": "Likely",
                    "urgency": "Immediate",
                    "event": "Hurricane Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Hurricane Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "A Hurricane Warning means hurricane-force winds are expected\nsomewhere within this area within the next 36 hours\n\n* LOCATIONS AFFECTED\n- Falfurrias\n- Encino\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Strong Tropical Storm force\nwind\n- Peak Wind Forecast: 45-60 mph with gusts to 75 mph\n- Window for Tropical Storm force winds: early Saturday\nafternoon until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 58\nto 73 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for dangerous wind of equivalent strong tropical\nstorm force.\n- PREPARE: Remaining efforts to protect life and property\nshould be completed as soon as possible. Prepare for\nsignificant wind damage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Significant\n- Some damage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 6-10 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "HURRICANE WARNING IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.NEW.KBRO.HU.W.1008.200725T0254Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "EAS",
                            "NWEM"
                        ],
                        "WEAHandling": [
                            "Imminent Threat"
                        ],
                        "CMAMlongtext": [
                            "National Weather Service: A HURRICANE WARNING is in effect for this area for dangerous and damaging winds. This warning is issued up to 36 hours before hazardous conditions begin. Urgently complete efforts to protect life and property. Have food, water, cash, fuel, and medications for 3+ days. FOLLOW INSTRUCTIONS FROM LOCAL OFFICIALS."
                        ],
                        "CMAMtext": [
                            "NWS: HURRICANE WARNING this area. Check media and local authorities."
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348429-3638970",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.3379999,
                                26.367000000000001
                            ],
                            [
                                -97.218000000000004,
                                26.393000000000001
                            ],
                            [
                                -97.13300000000001,
                                26.067
                            ],
                            [
                                -97.14800000000001,
                                25.952999999999999
                            ],
                            [
                                -97.159000000000006,
                                25.948999999999998
                            ],
                            [
                                -97.159000000000006,
                                25.962999999999997
                            ],
                            [
                                -97.176000000000002,
                                25.964999999999996
                            ],
                            [
                                -97.189999999999998,
                                25.953999999999997
                            ],
                            [
                                -97.2099999,
                                25.962999999999997
                            ],
                            [
                                -97.254000000000005,
                                25.948999999999998
                            ],
                            [
                                -97.363,
                                26.124999999999996
                            ],
                            [
                                -97.412999999999997,
                                26.218999999999998
                            ],
                            [
                                -97.456000000000003,
                                26.326999999999998
                            ],
                            [
                                -97.444999899999999,
                                26.325999999999997
                            ],
                            [
                                -97.432000000000002,
                                26.360999999999997
                            ],
                            [
                                -97.411000000000001,
                                26.374999999999996
                            ],
                            [
                                -97.400999999999996,
                                26.386999999999997
                            ],
                            [
                                -97.394999999999996,
                                26.401999999999997
                            ],
                            [
                                -97.382999999999996,
                                26.403999999999996
                            ],
                            [
                                -97.379999999999995,
                                26.409999999999997
                            ],
                            [
                                -97.3379999,
                                26.367000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348429-3638970",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348429-3638970",
                    "areaDesc": "Coastal Cameron",
                    "geocode": {
                        "UGC": [
                            "TXZ257"
                        ],
                        "SAME": [
                            "048061"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ257"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348070-3638770",
                            "identifier": "NWS-IDP-PROD-4348070-3638770",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T18:32:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347695-3638468",
                            "identifier": "NWS-IDP-PROD-4347695-3638468",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T15:59:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347167-3638169",
                            "identifier": "NWS-IDP-PROD-4347167-3638169",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:14:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346499-3637752",
                            "identifier": "NWS-IDP-PROD-4346499-3637752",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346578-3637814",
                            "identifier": "NWS-IDP-PROD-4346578-3637814",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:10:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346891-3638015",
                            "identifier": "NWS-IDP-PROD-4346891-3638015",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:52:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "* LOCATIONS AFFECTED\n- South Padre Island\n- Port Isabel\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 35-45 mph with gusts to 60 mph\n- Window for Tropical Storm force winds: early Saturday\nafternoon until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for up to 2 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Shelter against storm surge flooding greater than 1\nfoot above ground.\n- PREPARE: All flood preparations should be complete. Expect\nflooding of low-lying roads and property.\n- ACT: Stay away from storm surge prone areas. Continue to\nfollow the instructions of local officials.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 4-8 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KBRO.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348430-3638971",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -98.423000000000002,
                                26.783999999999999
                            ],
                            [
                                -98.320999999999998,
                                26.782999999999998
                            ],
                            [
                                -98.466999999999999,
                                26.493999999999996
                            ],
                            [
                                -98.483000000000004,
                                26.461999999999996
                            ],
                            [
                                -98.527000000000001,
                                26.374999999999996
                            ],
                            [
                                -98.585999999999999,
                                26.257999999999996
                            ],
                            [
                                -98.599999999999994,
                                26.256999999999994
                            ],
                            [
                                -98.61699999999999,
                                26.246999999999993
                            ],
                            [
                                -98.62299999999999,
                                26.258999999999993
                            ],
                            [
                                -98.633999999999986,
                                26.242999999999995
                            ],
                            [
                                -98.669999999999987,
                                26.236999899999994
                            ],
                            [
                                -98.677999999999983,
                                26.242999999999995
                            ],
                            [
                                -98.681999999999988,
                                26.262999999999995
                            ],
                            [
                                -98.718999999999994,
                                26.272999999999996
                            ],
                            [
                                -98.7159999,
                                26.278999999999996
                            ],
                            [
                                -98.700999899999999,
                                26.278999999999996
                            ],
                            [
                                -98.703999899999999,
                                26.287999999999997
                            ],
                            [
                                -98.715000000000003,
                                26.285999999999998
                            ],
                            [
                                -98.728999999999999,
                                26.298999999999999
                            ],
                            [
                                -98.75,
                                26.295999999999999
                            ],
                            [
                                -98.754999999999995,
                                26.308
                            ],
                            [
                                -98.741,
                                26.303000000000001
                            ],
                            [
                                -98.736000000000004,
                                26.307000000000002
                            ],
                            [
                                -98.75,
                                26.329999900000001
                            ],
                            [
                                -98.771000000000001,
                                26.324999999999999
                            ],
                            [
                                -98.789000000000001,
                                26.331
                            ],
                            [
                                -98.798000000000002,
                                26.359999999999999
                            ],
                            [
                                -98.807000000000002,
                                26.369
                            ],
                            [
                                -98.822999899999999,
                                26.370999999999999
                            ],
                            [
                                -98.841999999999999,
                                26.358999999999998
                            ],
                            [
                                -98.861000000000004,
                                26.366
                            ],
                            [
                                -98.896000000000001,
                                26.352999999999998
                            ],
                            [
                                -98.900999999999996,
                                26.370999999999999
                            ],
                            [
                                -98.921999999999997,
                                26.378999999999998
                            ],
                            [
                                -98.926999999999992,
                                26.393999899999997
                            ],
                            [
                                -98.934999999999988,
                                26.385999999999996
                            ],
                            [
                                -98.935999999999993,
                                26.371999999999996
                            ],
                            [
                                -98.941999899999999,
                                26.369999999999997
                            ],
                            [
                                -98.956000000000003,
                                26.377999999999997
                            ],
                            [
                                -98.953999899999999,
                                26.392999999999997
                            ],
                            [
                                -98.974000000000004,
                                26.400999999999996
                            ],
                            [
                                -98.990000000000009,
                                26.391999999999996
                            ],
                            [
                                -99.010000000000005,
                                26.391999999999996
                            ],
                            [
                                -99.022000000000006,
                                26.407999999999994
                            ],
                            [
                                -99.040000000000006,
                                26.412999999999993
                            ],
                            [
                                -99.063000000000002,
                                26.396999899999994
                            ],
                            [
                                -99.084000000000003,
                                26.397999999999993
                            ],
                            [
                                -99.113,
                                26.433999999999994
                            ],
                            [
                                -99.102999999999994,
                                26.441999999999993
                            ],
                            [
                                -99.091999999999999,
                                26.476999999999993
                            ],
                            [
                                -99.126999999999995,
                                26.523999999999994
                            ],
                            [
                                -99.170000000000002,
                                26.538999999999994
                            ],
                            [
                                -99.168999999999997,
                                26.571999999999996
                            ],
                            [
                                -99.010999999999996,
                                26.674999999999997
                            ],
                            [
                                -98.953999899999999,
                                26.785999999999998
                            ],
                            [
                                -98.423000000000002,
                                26.783999999999999
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348430-3638971",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348430-3638971",
                    "areaDesc": "Starr",
                    "geocode": {
                        "UGC": [
                            "TXZ252"
                        ],
                        "SAME": [
                            "048427"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ252"
                    ],
                    "references": [],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "A Tropical Storm Warning means tropical storm-force winds are\nexpected somewhere within this area within the next 36 hours\n\n* LOCATIONS AFFECTED\n- Rio Grande City\n- Roma\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 40-50 mph with gusts to 65 mph\n- Window for Tropical Storm force winds: early Saturday\nafternoon until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 58\nto 73 mph\n- The wind threat has increased from the previous assessment.\n- PLAN: Plan for dangerous wind of equivalent strong tropical\nstorm force.\n- PREPARE: Remaining efforts to protect life and property\nshould be completed as soon as possible. Prepare for\nsignificant wind damage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Significant\n- Some damage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 4-8 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is unfavorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Tornadoes not expected\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Tornadoes are not expected. Showers and thunderstorms\nwith gusty winds may still occur.\n- PREPARE: Little to no preparations needed to protect\nagainst tornadoes at this time. Keep informed of the latest\ntornado situation.\n- ACT: Listen for changes in the forecast.\n\n- POTENTIAL IMPACTS: Little to None\n- Little to no potential impacts from tornadoes.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.EXA.KBRO.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348434-3638976",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.528000000000006,
                                26.298999999999999
                            ],
                            [
                                -97.521000000000001,
                                26.326000000000001
                            ],
                            [
                                -97.507000000000005,
                                26.321999999999999
                            ],
                            [
                                -97.513000000000005,
                                26.312999999999999
                            ],
                            [
                                -97.501000000000005,
                                26.318999999999999
                            ],
                            [
                                -97.50800000000001,
                                26.334
                            ],
                            [
                                -97.484000000000009,
                                26.337
                            ],
                            [
                                -97.470000000000013,
                                26.329999900000001
                            ],
                            [
                                -97.475000000000009,
                                26.34
                            ],
                            [
                                -97.470000000000013,
                                26.343
                            ],
                            [
                                -97.464000000000013,
                                26.332000000000001
                            ],
                            [
                                -97.458000000000013,
                                26.332000000000001
                            ],
                            [
                                -97.456000000000017,
                                26.327000000000002
                            ],
                            [
                                -97.413000000000011,
                                26.219000000000001
                            ],
                            [
                                -97.363000000000014,
                                26.125
                            ],
                            [
                                -97.254000000000019,
                                25.949000000000002
                            ],
                            [
                                -97.277000000000015,
                                25.952000000000002
                            ],
                            [
                                -97.27800000000002,
                                25.946000000000002
                            ],
                            [
                                -97.277000000000015,
                                25.936
                            ],
                            [
                                -97.301000000000016,
                                25.937000000000001
                            ],
                            [
                                -97.310000000000016,
                                25.927
                            ],
                            [
                                -97.318000000000012,
                                25.931000000000001
                            ],
                            [
                                -97.328000000000017,
                                25.917999999999999
                            ],
                            [
                                -97.333000000000013,
                                25.925999900000001
                            ],
                            [
                                -97.337999900000014,
                                25.920999999999999
                            ],
                            [
                                -97.337999900000014,
                                25.928999900000001
                            ],
                            [
                                -97.348000000000013,
                                25.931000000000001
                            ],
                            [
                                -97.355000000000018,
                                25.919
                            ],
                            [
                                -97.374000000000024,
                                25.908000000000001
                            ],
                            [
                                -97.366000000000028,
                                25.902000000000001
                            ],
                            [
                                -97.364000000000033,
                                25.890000000000001
                            ],
                            [
                                -97.357000000000028,
                                25.888000000000002
                            ],
                            [
                                -97.373000000000033,
                                25.879000000000001
                            ],
                            [
                                -97.359000000000037,
                                25.879000000000001
                            ],
                            [
                                -97.358000000000033,
                                25.870000000000001
                            ],
                            [
                                -97.376000000000033,
                                25.855
                            ],
                            [
                                -97.365000000000038,
                                25.853000000000002
                            ],
                            [
                                -97.373000000000033,
                                25.841000000000001
                            ],
                            [
                                -97.401000000000039,
                                25.84
                            ],
                            [
                                -97.400000000000034,
                                25.850999999999999
                            ],
                            [
                                -97.409000000000034,
                                25.846999999999998
                            ],
                            [
                                -97.409000000000034,
                                25.860999999999997
                            ],
                            [
                                -97.413000000000039,
                                25.841999999999999
                            ],
                            [
                                -97.42500000000004,
                                25.840999999999998
                            ],
                            [
                                -97.44300000000004,
                                25.848999999999997
                            ],
                            [
                                -97.444999900000042,
                                25.855999999999998
                            ],
                            [
                                -97.453000000000046,
                                25.853999999999999
                            ],
                            [
                                -97.444999900000042,
                                25.867999999999999
                            ],
                            [
                                -97.449000000000041,
                                25.872
                            ],
                            [
                                -97.455000000000041,
                                25.867000000000001
                            ],
                            [
                                -97.495000000000047,
                                25.880000000000003
                            ],
                            [
                                -97.498000000000047,
                                25.899000000000001
                            ],
                            [
                                -97.521000000000043,
                                25.885999999999999
                            ],
                            [
                                -97.534000000000049,
                                25.910999999999998
                            ],
                            [
                                -97.530000000000044,
                                25.918999999999997
                            ],
                            [
                                -97.543000000000049,
                                25.919999999999998
                            ],
                            [
                                -97.550000000000054,
                                25.935999999999996
                            ],
                            [
                                -97.559000000000054,
                                25.931999999999995
                            ],
                            [
                                -97.581999900000056,
                                25.937999999999995
                            ],
                            [
                                -97.57800000000006,
                                25.941999999999997
                            ],
                            [
                                -97.581999900000056,
                                25.961999999999996
                            ],
                            [
                                -97.602000000000061,
                                25.957999899999997
                            ],
                            [
                                -97.610000000000056,
                                25.966999999999999
                            ],
                            [
                                -97.609000000000052,
                                25.977
                            ],
                            [
                                -97.628000000000057,
                                25.988
                            ],
                            [
                                -97.635000000000062,
                                26
                            ],
                            [
                                -97.648000000000067,
                                26.009
                            ],
                            [
                                -97.638000000000062,
                                26.013999999999999
                            ],
                            [
                                -97.641000000000062,
                                26.024000000000001
                            ],
                            [
                                -97.648000000000067,
                                26.026
                            ],
                            [
                                -97.651000000000067,
                                26.016999999999999
                            ],
                            [
                                -97.668000000000063,
                                26.018999900000001
                            ],
                            [
                                -97.678000000000068,
                                26.026
                            ],
                            [
                                -97.693000000000069,
                                26.032
                            ],
                            [
                                -97.693000000000069,
                                26.02
                            ],
                            [
                                -97.706999900000071,
                                26.036999999999999
                            ],
                            [
                                -97.709999900000071,
                                26.026
                            ],
                            [
                                -97.718000000000075,
                                26.024000000000001
                            ],
                            [
                                -97.738000000000071,
                                26.021999900000001
                            ],
                            [
                                -97.760000000000076,
                                26.026
                            ],
                            [
                                -97.778000000000077,
                                26.030000000000001
                            ],
                            [
                                -97.795000000000073,
                                26.037000000000003
                            ],
                            [
                                -97.796000000000078,
                                26.045000000000002
                            ],
                            [
                                -97.790000000000077,
                                26.050999900000001
                            ],
                            [
                                -97.801000000000073,
                                26.060000000000002
                            ],
                            [
                                -97.810000000000073,
                                26.057000000000002
                            ],
                            [
                                -97.813000000000073,
                                26.045000000000002
                            ],
                            [
                                -97.818000000000069,
                                26.056000000000001
                            ],
                            [
                                -97.834999900000071,
                                26.047000000000001
                            ],
                            [
                                -97.86000000000007,
                                26.053000000000001
                            ],
                            [
                                -97.862000000000066,
                                26.07
                            ],
                            [
                                -97.862000000000066,
                                26.347999999999999
                            ],
                            [
                                -97.528000000000006,
                                26.298999999999999
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348434-3638976",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348434-3638976",
                    "areaDesc": "Inland Cameron",
                    "geocode": {
                        "UGC": [
                            "TXZ255"
                        ],
                        "SAME": [
                            "048061"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ255"
                    ],
                    "references": [],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "A Tropical Storm Warning means tropical storm-force winds are\nexpected somewhere within this area within the next 36 hours\n\n* LOCATIONS AFFECTED\n- Brownsville\n- Harlingen\n- La Feria\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 35-45 mph with gusts to 55 mph\n- Window for Tropical Storm force winds: early Saturday\nafternoon until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for up to 2 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has increased from the previous\nassessment.\n- PLAN: Plan for storm surge flooding greater than 1 foot\nabove ground.\n- PREPARE: Complete preparations for storm surge flooding,\nespecially in low-lying vulnerable areas, before conditions\nbecome unsafe.\n- ACT: Leave immediately if evacuation orders are given for\nyour area.\n\n- POTENTIAL IMPACTS: Limited\n- Localized inundation with storm surge flooding mainly along\nimmediate shorelines and in low-lying spots, or in areas\nfarther inland near where higher surge waters move ashore.\n- Sections of near-shore roads and parking lots become\noverspread with surge water. Driving conditions dangerous\nin places where surge water covers the road.\n- Moderate beach erosion. Heavy surf also breaching dunes,\nmainly in usually vulnerable locations. Strong rip currents.\n- Minor to locally moderate damage to marinas, docks,\nboardwalks, and piers. A few small craft broken away from\nmoorings.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 4-8 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.EXA.KBRO.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348433-3638975",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.530000000000001,
                                26.600999999999999
                            ],
                            [
                                -97.519999999999996,
                                26.491999999999997
                            ],
                            [
                                -97.457999999999998,
                                26.331999999999997
                            ],
                            [
                                -97.463999999999999,
                                26.331999999999997
                            ],
                            [
                                -97.469999999999999,
                                26.342999999999996
                            ],
                            [
                                -97.474999999999994,
                                26.339999999999996
                            ],
                            [
                                -97.469999999999999,
                                26.329999899999997
                            ],
                            [
                                -97.483999999999995,
                                26.336999999999996
                            ],
                            [
                                -97.507999999999996,
                                26.333999999999996
                            ],
                            [
                                -97.500999999999991,
                                26.318999999999996
                            ],
                            [
                                -97.512999999999991,
                                26.312999999999995
                            ],
                            [
                                -97.506999999999991,
                                26.321999999999996
                            ],
                            [
                                -97.520999999999987,
                                26.325999999999997
                            ],
                            [
                                -97.527999999999992,
                                26.298999999999996
                            ],
                            [
                                -97.861999999999995,
                                26.347999999999995
                            ],
                            [
                                -97.861999999999995,
                                26.390999899999997
                            ],
                            [
                                -97.861999999999995,
                                26.393999899999997
                            ],
                            [
                                -97.861999999999995,
                                26.405999999999999
                            ],
                            [
                                -97.861999999999995,
                                26.411999999999999
                            ],
                            [
                                -97.861999999999995,
                                26.433999999999997
                            ],
                            [
                                -97.908000000000001,
                                26.433999999999997
                            ],
                            [
                                -97.989000000000004,
                                26.445999999999998
                            ],
                            [
                                -98.004000000000005,
                                26.448999999999998
                            ],
                            [
                                -97.984000000000009,
                                26.536999999999999
                            ],
                            [
                                -97.964000000000013,
                                26.533999999999999
                            ],
                            [
                                -97.968000000000018,
                                26.568999999999999
                            ],
                            [
                                -97.956999900000014,
                                26.611999900000001
                            ],
                            [
                                -97.861000000000018,
                                26.597999999999999
                            ],
                            [
                                -97.558000000000021,
                                26.599999999999998
                            ],
                            [
                                -97.536000000000016,
                                26.600999999999999
                            ],
                            [
                                -97.530000000000001,
                                26.600999999999999
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348433-3638975",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348433-3638975",
                    "areaDesc": "Inland Willacy",
                    "geocode": {
                        "UGC": [
                            "TXZ254"
                        ],
                        "SAME": [
                            "048489"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ254"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348068-3638768",
                            "identifier": "NWS-IDP-PROD-4348068-3638768",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T18:32:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346505-3637758",
                            "identifier": "NWS-IDP-PROD-4346505-3637758",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346897-3638021",
                            "identifier": "NWS-IDP-PROD-4346897-3638021",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:52:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346575-3637811",
                            "identifier": "NWS-IDP-PROD-4346575-3637811",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:10:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347697-3638470",
                            "identifier": "NWS-IDP-PROD-4347697-3638470",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T15:59:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347162-3638164",
                            "identifier": "NWS-IDP-PROD-4347162-3638164",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:14:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "* LOCATIONS AFFECTED\n- Raymondville\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 45-55 mph with gusts to 75 mph\n- Window for Tropical Storm force winds: early Saturday\nafternoon until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 58\nto 73 mph\n- The wind threat has increased from the previous assessment.\n- PLAN: Plan for dangerous wind of equivalent strong tropical\nstorm force.\n- PREPARE: Remaining efforts to protect life and property\nshould be completed as soon as possible. Prepare for\nsignificant wind damage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Significant\n- Some damage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* STORM SURGE\n- No storm surge inundation forecast\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Little to no storm\nsurge flooding\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: There is little to no threat of storm surge flooding.\nRough surf, coastal erosion, and life-threatening rip\ncurrents are possible.\n- PREPARE: Little to no preparations for storm surge flooding\nare needed.\n- ACT: Follow the instructions of local officials. Monitor\nforecasts.\n\n- POTENTIAL IMPACTS: Little to None\n- Little to no potential impacts from storm surge flooding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 6-10 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KBRO.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348435-3638978",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.632000000000005,
                                27.242999999999999
                            ],
                            [
                                -97.594999999999999,
                                27.206999999999997
                            ],
                            [
                                -97.5849999,
                                27.185999999999996
                            ],
                            [
                                -97.581000000000003,
                                27.159999999999997
                            ],
                            [
                                -97.572999899999999,
                                27.075999999999997
                            ],
                            [
                                -97.579999999999998,
                                27.029999999999998
                            ],
                            [
                                -97.605000000000004,
                                26.965999999999998
                            ],
                            [
                                -97.609999999999999,
                                26.903999999999996
                            ],
                            [
                                -97.596999999999994,
                                26.826999999999995
                            ],
                            [
                                -97.549999999999997,
                                26.720999999999993
                            ],
                            [
                                -97.533999999999992,
                                26.657999999999994
                            ],
                            [
                                -97.529999999999987,
                                26.600999999999996
                            ],
                            [
                                -97.535999999999987,
                                26.600999999999996
                            ],
                            [
                                -97.557999999999993,
                                26.599999999999994
                            ],
                            [
                                -97.86099999999999,
                                26.597999999999995
                            ],
                            [
                                -97.956999899999985,
                                26.611999899999997
                            ],
                            [
                                -97.984999999999985,
                                26.615999999999996
                            ],
                            [
                                -97.984999999999985,
                                26.780999999999995
                            ],
                            [
                                -97.984999999999985,
                                27.208999999999996
                            ],
                            [
                                -97.959999899999985,
                                27.213999999999995
                            ],
                            [
                                -97.951999999999984,
                                27.232999999999993
                            ],
                            [
                                -97.922999999999988,
                                27.237999999999992
                            ],
                            [
                                -97.919999999999987,
                                27.242999999999991
                            ],
                            [
                                -97.912999999999982,
                                27.237999999999992
                            ],
                            [
                                -97.895999999999987,
                                27.241999999999994
                            ],
                            [
                                -97.884999999999991,
                                27.235999999999994
                            ],
                            [
                                -97.855999999999995,
                                27.244999999999994
                            ],
                            [
                                -97.855999999999995,
                                27.250999999999994
                            ],
                            [
                                -97.8409999,
                                27.243999999999993
                            ],
                            [
                                -97.816999899999999,
                                27.253999999999994
                            ],
                            [
                                -97.814999999999998,
                                27.271999999999995
                            ],
                            [
                                -97.796999999999997,
                                27.271999999999995
                            ],
                            [
                                -97.795000000000002,
                                27.274999999999995
                            ],
                            [
                                -97.784999999999997,
                                27.283999999999995
                            ],
                            [
                                -97.768000000000001,
                                27.275999999999996
                            ],
                            [
                                -97.757999999999996,
                                27.281999999999996
                            ],
                            [
                                -97.727999999999994,
                                27.257999999999996
                            ],
                            [
                                -97.7099999,
                                27.267999999999997
                            ],
                            [
                                -97.691999899999999,
                                27.266999999999996
                            ],
                            [
                                -97.647999999999996,
                                27.275999999999996
                            ],
                            [
                                -97.640000000000001,
                                27.269999999999996
                            ],
                            [
                                -97.640000000000001,
                                27.252999999999997
                            ],
                            [
                                -97.632000000000005,
                                27.242999999999999
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348435-3638978",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348435-3638978",
                    "areaDesc": "Coastal Kenedy",
                    "geocode": {
                        "UGC": [
                            "TXZ351"
                        ],
                        "SAME": [
                            "048261"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ351"
                    ],
                    "references": [],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Extreme",
                    "certainty": "Likely",
                    "urgency": "Immediate",
                    "event": "Hurricane Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Hurricane Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "A Hurricane Warning means hurricane-force winds are expected\nsomewhere within this area within the next 36 hours\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Strong Tropical Storm force\nwind\n- Peak Wind Forecast: 55-70 mph with gusts to 85 mph\n- Window for Tropical Storm force winds: Saturday morning\nuntil early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 58\nto 73 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for dangerous wind of equivalent strong tropical\nstorm force.\n- PREPARE: Remaining efforts to protect life and property\nshould be completed as soon as possible. Prepare for\nsignificant wind damage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Significant\n- Some damage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for up to 2 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Shelter against storm surge flooding greater than 1\nfoot above ground.\n- PREPARE: All flood preparations should be complete. Expect\nflooding of low-lying roads and property.\n- ACT: Stay away from storm surge prone areas. Continue to\nfollow the instructions of local officials.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 6-10 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "HURRICANE WARNING IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.NEW.KBRO.HU.W.1008.200725T0254Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "EAS",
                            "NWEM"
                        ],
                        "WEAHandling": [
                            "Imminent Threat"
                        ],
                        "CMAMlongtext": [
                            "National Weather Service: A HURRICANE WARNING is in effect for this area for dangerous and damaging winds. This warning is issued up to 36 hours before hazardous conditions begin. Urgently complete efforts to protect life and property. Have food, water, cash, fuel, and medications for 3+ days. FOLLOW INSTRUCTIONS FROM LOCAL OFFICIALS."
                        ],
                        "CMAMtext": [
                            "NWS: HURRICANE WARNING this area. Check media and local authorities."
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348439-3638983",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -98.524000000000001,
                                27.265000000000001
                            ],
                            [
                                -98.536000000000001,
                                27.263999999999999
                            ],
                            [
                                -98.531000000000006,
                                27.254999999999999
                            ],
                            [
                                -98.512,
                                27.250999999999998
                            ],
                            [
                                -98.507000000000005,
                                27.239999999999998
                            ],
                            [
                                -98.493000000000009,
                                27.234999999999999
                            ],
                            [
                                -98.493000000000009,
                                27.141999999999999
                            ],
                            [
                                -98.467000000000013,
                                27.140999999999998
                            ],
                            [
                                -98.465999900000014,
                                27.055
                            ],
                            [
                                -98.418000000000021,
                                27.055
                            ],
                            [
                                -98.423000000000016,
                                26.783999999999999
                            ],
                            [
                                -98.953999900000014,
                                26.785999999999998
                            ],
                            [
                                -98.955000000000013,
                                27.268999999999998
                            ],
                            [
                                -98.798000000000016,
                                27.267999999999997
                            ],
                            [
                                -98.798000000000016,
                                27.353999999999996
                            ],
                            [
                                -98.625000000000014,
                                27.357999999999997
                            ],
                            [
                                -98.625000000000014,
                                27.337999999999997
                            ],
                            [
                                -98.589000000000013,
                                27.337999999999997
                            ],
                            [
                                -98.589000000000013,
                                27.358999999999998
                            ],
                            [
                                -98.553000000000011,
                                27.358999999999998
                            ],
                            [
                                -98.552000000000007,
                                27.343999999999998
                            ],
                            [
                                -98.52300000000001,
                                27.342999999999996
                            ],
                            [
                                -98.524000000000001,
                                27.265000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348439-3638983",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348439-3638983",
                    "areaDesc": "Jim Hogg",
                    "geocode": {
                        "UGC": [
                            "TXZ249"
                        ],
                        "SAME": [
                            "048247"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ249"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346577-3637813",
                            "identifier": "NWS-IDP-PROD-4346577-3637813",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:10:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346892-3638016",
                            "identifier": "NWS-IDP-PROD-4346892-3638016",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:52:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347168-3638170",
                            "identifier": "NWS-IDP-PROD-4347168-3638170",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:14:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346503-3637756",
                            "identifier": "NWS-IDP-PROD-4346503-3637756",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347696-3638469",
                            "identifier": "NWS-IDP-PROD-4347696-3638469",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T15:59:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348075-3638775",
                            "identifier": "NWS-IDP-PROD-4348075-3638775",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T18:32:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "* LOCATIONS AFFECTED\n- Hebbronville\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 40-50 mph with gusts to 65 mph\n- Window for Tropical Storm force winds: early Saturday\nafternoon until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 58\nto 73 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for dangerous wind of equivalent strong tropical\nstorm force.\n- PREPARE: Remaining efforts to protect life and property\nshould be completed as soon as possible. Prepare for\nsignificant wind damage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Significant\n- Some damage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 4-8 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is unfavorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Tornadoes not expected\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Tornadoes are not expected. Showers and thunderstorms\nwith gusty winds may still occur.\n- PREPARE: Little to no preparations needed to protect\nagainst tornadoes at this time. Keep informed of the latest\ntornado situation.\n- ACT: Listen for changes in the forecast.\n\n- POTENTIAL IMPACTS: Little to None\n- Little to no potential impacts from tornadoes.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KBRO.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348431-3638972",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.265000000000001,
                                26.539999999999999
                            ],
                            [
                                -97.236999999999995,
                                26.462
                            ],
                            [
                                -97.217999999999989,
                                26.393000000000001
                            ],
                            [
                                -97.337999899999986,
                                26.367000000000001
                            ],
                            [
                                -97.379999999999981,
                                26.41
                            ],
                            [
                                -97.382999999999981,
                                26.404
                            ],
                            [
                                -97.394999999999982,
                                26.402000000000001
                            ],
                            [
                                -97.400999999999982,
                                26.387
                            ],
                            [
                                -97.410999999999987,
                                26.375
                            ],
                            [
                                -97.431999999999988,
                                26.361000000000001
                            ],
                            [
                                -97.444999899999985,
                                26.326000000000001
                            ],
                            [
                                -97.455999999999989,
                                26.327000000000002
                            ],
                            [
                                -97.457999999999984,
                                26.332000000000001
                            ],
                            [
                                -97.519999999999982,
                                26.492000000000001
                            ],
                            [
                                -97.529999999999987,
                                26.601000000000003
                            ],
                            [
                                -97.446999999999989,
                                26.600000000000001
                            ],
                            [
                                -97.416999999999987,
                                26.591000000000001
                            ],
                            [
                                -97.400999999999982,
                                26.542000000000002
                            ],
                            [
                                -97.362999999999985,
                                26.542000000000002
                            ],
                            [
                                -97.301999999999978,
                                26.543000000000003
                            ],
                            [
                                -97.265000000000001,
                                26.539999999999999
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348431-3638972",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348431-3638972",
                    "areaDesc": "Coastal Willacy",
                    "geocode": {
                        "UGC": [
                            "TXZ256"
                        ],
                        "SAME": [
                            "048489"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ256"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346579-3637815",
                            "identifier": "NWS-IDP-PROD-4346579-3637815",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:10:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346896-3638020",
                            "identifier": "NWS-IDP-PROD-4346896-3638020",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:52:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347166-3638168",
                            "identifier": "NWS-IDP-PROD-4347166-3638168",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:14:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346498-3637751",
                            "identifier": "NWS-IDP-PROD-4346498-3637751",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346498-3637750",
                            "identifier": "NWS-IDP-PROD-4346498-3637750",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348071-3638771",
                            "identifier": "NWS-IDP-PROD-4348071-3638771",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T18:32:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347698-3638471",
                            "identifier": "NWS-IDP-PROD-4347698-3638471",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T15:59:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "* LOCATIONS AFFECTED\n- Port Mansfield\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Strong Tropical Storm force\nwind\n- Peak Wind Forecast: 50-65 mph with gusts to 80 mph\n- Window for Tropical Storm force winds: late Saturday\nmorning until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 58\nto 73 mph\n- The wind threat has increased from the previous assessment.\n- PLAN: Plan for dangerous wind of equivalent strong tropical\nstorm force.\n- PREPARE: Remaining efforts to protect life and property\nshould be completed as soon as possible. Prepare for\nsignificant wind damage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Significant\n- Some damage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for up to 2 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Shelter against storm surge flooding greater than 1\nfoot above ground.\n- PREPARE: All flood preparations should be complete. Expect\nflooding of low-lying roads and property.\n- ACT: Stay away from storm surge prone areas. Continue to\nfollow the instructions of local officials.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 4-8 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KBRO.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348436-3638979",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.989000000000004,
                                26.446000000000002
                            ],
                            [
                                -97.989000000000004,
                                26.440000000000001
                            ],
                            [
                                -98.466999999999999,
                                26.494
                            ],
                            [
                                -98.320999999999998,
                                26.783000000000001
                            ],
                            [
                                -97.984999999999999,
                                26.781000000000002
                            ],
                            [
                                -97.984999999999999,
                                26.616000000000003
                            ],
                            [
                                -97.9569999,
                                26.611999900000004
                            ],
                            [
                                -97.968000000000004,
                                26.569000000000003
                            ],
                            [
                                -97.963999999999999,
                                26.534000000000002
                            ],
                            [
                                -97.983999999999995,
                                26.537000000000003
                            ],
                            [
                                -98.003999999999991,
                                26.449000000000002
                            ],
                            [
                                -97.989000000000004,
                                26.446000000000002
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348436-3638979",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348436-3638979",
                    "areaDesc": "Southern Hidalgo",
                    "geocode": {
                        "UGC": [
                            "TXZ253"
                        ],
                        "SAME": [
                            "048215"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ253"
                    ],
                    "references": [],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "A Tropical Storm Warning means tropical storm-force winds are\nexpected somewhere within this area within the next 36 hours\n\n* LOCATIONS AFFECTED\n- McAllen\n- Edinburg\n- Weslaco\n- Mission\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 35-45 mph with gusts to 60 mph\n- Window for Tropical Storm force winds: early Saturday\nafternoon until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 6-10 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.EXA.KBRO.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348440-3638984",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.989000000000004,
                                26.440000000000001
                            ],
                            [
                                -97.989000000000004,
                                26.446000000000002
                            ],
                            [
                                -97.908000000000001,
                                26.434000000000001
                            ],
                            [
                                -97.861999999999995,
                                26.434000000000001
                            ],
                            [
                                -97.861999999999995,
                                26.412000000000003
                            ],
                            [
                                -97.861999999999995,
                                26.406000000000002
                            ],
                            [
                                -97.861999999999995,
                                26.393999900000001
                            ],
                            [
                                -97.861999999999995,
                                26.390999900000001
                            ],
                            [
                                -97.861999999999995,
                                26.347999999999999
                            ],
                            [
                                -97.861999999999995,
                                26.07
                            ],
                            [
                                -97.86999999999999,
                                26.058
                            ],
                            [
                                -97.883999999999986,
                                26.065999999999999
                            ],
                            [
                                -97.926999999999992,
                                26.055999999999997
                            ],
                            [
                                -97.932999999999993,
                                26.064999999999998
                            ],
                            [
                                -97.934999999999988,
                                26.052999999999997
                            ],
                            [
                                -97.949999999999989,
                                26.061999999999998
                            ],
                            [
                                -97.965999899999986,
                                26.051999999999996
                            ],
                            [
                                -97.98099999999998,
                                26.066999999999997
                            ],
                            [
                                -97.991999999999976,
                                26.058999999999997
                            ],
                            [
                                -97.999999999999972,
                                26.064999999999998
                            ],
                            [
                                -98.010999999999967,
                                26.057999999999996
                            ],
                            [
                                -98.011999999999972,
                                26.065999999999995
                            ],
                            [
                                -98.019999999999968,
                                26.058999999999994
                            ],
                            [
                                -98.026999999999973,
                                26.065999999999995
                            ],
                            [
                                -98.038999999999973,
                                26.041999999999994
                            ],
                            [
                                -98.060999999999979,
                                26.045999999999996
                            ],
                            [
                                -98.073999999999984,
                                26.035999999999994
                            ],
                            [
                                -98.078999899999985,
                                26.041999999999994
                            ],
                            [
                                -98.069999899999985,
                                26.051999999999996
                            ],
                            [
                                -98.083999999999989,
                                26.061999999999998
                            ],
                            [
                                -98.093999999999994,
                                26.058999999999997
                            ],
                            [
                                -98.10499999999999,
                                26.066999999999997
                            ],
                            [
                                -98.127999999999986,
                                26.061999999999998
                            ],
                            [
                                -98.145999999999987,
                                26.049999999999997
                            ],
                            [
                                -98.152999999999992,
                                26.057999999999996
                            ],
                            [
                                -98.161999999999992,
                                26.054999999999996
                            ],
                            [
                                -98.158999999999992,
                                26.063999999999997
                            ],
                            [
                                -98.167999999999992,
                                26.062999999999995
                            ],
                            [
                                -98.178999999999988,
                                26.062999999999995
                            ],
                            [
                                -98.186999999999983,
                                26.063999999999997
                            ],
                            [
                                -98.196999999999989,
                                26.055999999999997
                            ],
                            [
                                -98.220999999999989,
                                26.076999999999998
                            ],
                            [
                                -98.248999999999995,
                                26.073999999999998
                            ],
                            [
                                -98.284999999999997,
                                26.100999999999999
                            ],
                            [
                                -98.283999999999992,
                                26.106999999999999
                            ],
                            [
                                -98.269999999999996,
                                26.106999999999999
                            ],
                            [
                                -98.265999999999991,
                                26.120000000000001
                            ],
                            [
                                -98.274999999999991,
                                26.116
                            ],
                            [
                                -98.295999999999992,
                                26.120000000000001
                            ],
                            [
                                -98.302999999999997,
                                26.109999999999999
                            ],
                            [
                                -98.299999999999997,
                                26.102
                            ],
                            [
                                -98.305999999999997,
                                26.105
                            ],
                            [
                                -98.3349999,
                                26.137
                            ],
                            [
                                -98.328000000000003,
                                26.143000000000001
                            ],
                            [
                                -98.3379999,
                                26.151
                            ],
                            [
                                -98.332999999999998,
                                26.161000000000001
                            ],
                            [
                                -98.337000000000003,
                                26.166
                            ],
                            [
                                -98.347000000000008,
                                26.164999999999999
                            ],
                            [
                                -98.351000000000013,
                                26.151999999999997
                            ],
                            [
                                -98.360000000000014,
                                26.171999999999997
                            ],
                            [
                                -98.367000000000019,
                                26.167999999999996
                            ],
                            [
                                -98.367000000000019,
                                26.157999999999994
                            ],
                            [
                                -98.387000000000015,
                                26.157999999999994
                            ],
                            [
                                -98.402000000000015,
                                26.171999999999993
                            ],
                            [
                                -98.405000000000015,
                                26.182999999999993
                            ],
                            [
                                -98.419000000000011,
                                26.184999999999992
                            ],
                            [
                                -98.444000000000017,
                                26.20099999999999
                            ],
                            [
                                -98.438999900000013,
                                26.213999999999992
                            ],
                            [
                                -98.443000000000012,
                                26.222999999999992
                            ],
                            [
                                -98.455000000000013,
                                26.216999999999992
                            ],
                            [
                                -98.459999900000014,
                                26.225999999999992
                            ],
                            [
                                -98.480000000000018,
                                26.219999999999992
                            ],
                            [
                                -98.478000000000023,
                                26.203999999999994
                            ],
                            [
                                -98.483000000000018,
                                26.201999999999995
                            ],
                            [
                                -98.484000000000023,
                                26.211999999999996
                            ],
                            [
                                -98.507000000000019,
                                26.209999999999997
                            ],
                            [
                                -98.502000000000024,
                                26.221999999999998
                            ],
                            [
                                -98.513000000000019,
                                26.226999999999997
                            ],
                            [
                                -98.524000000000015,
                                26.221999999999998
                            ],
                            [
                                -98.52200000000002,
                                26.234999999999999
                            ],
                            [
                                -98.536000000000016,
                                26.225999999999999
                            ],
                            [
                                -98.545000000000016,
                                26.244
                            ],
                            [
                                -98.555000000000021,
                                26.247
                            ],
                            [
                                -98.559000000000026,
                                26.245000000000001
                            ],
                            [
                                -98.546000000000021,
                                26.236000000000001
                            ],
                            [
                                -98.561000000000021,
                                26.225000000000001
                            ],
                            [
                                -98.566999900000027,
                                26.241
                            ],
                            [
                                -98.578999900000028,
                                26.233999999999998
                            ],
                            [
                                -98.584999900000028,
                                26.244
                            ],
                            [
                                -98.580000000000027,
                                26.254000000000001
                            ],
                            [
                                -98.586000000000027,
                                26.258000000000003
                            ],
                            [
                                -98.527000000000029,
                                26.375000000000004
                            ],
                            [
                                -98.483000000000033,
                                26.462000000000003
                            ],
                            [
                                -98.467000000000027,
                                26.494000000000003
                            ],
                            [
                                -97.989000000000004,
                                26.440000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348440-3638984",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348440-3638984",
                    "areaDesc": "Northern Hidalgo",
                    "geocode": {
                        "UGC": [
                            "TXZ353"
                        ],
                        "SAME": [
                            "048215"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ353"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346572-3637808",
                            "identifier": "NWS-IDP-PROD-4346572-3637808",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:10:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346893-3638017",
                            "identifier": "NWS-IDP-PROD-4346893-3638017",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:52:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347693-3638466",
                            "identifier": "NWS-IDP-PROD-4347693-3638466",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T15:59:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347169-3638171",
                            "identifier": "NWS-IDP-PROD-4347169-3638171",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:14:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348074-3638774",
                            "identifier": "NWS-IDP-PROD-4348074-3638774",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T18:32:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346500-3637753",
                            "identifier": "NWS-IDP-PROD-4346500-3637753",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 40-50 mph with gusts to 65 mph\n- Window for Tropical Storm force winds: early Saturday\nafternoon until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 58\nto 73 mph\n- The wind threat has increased from the previous assessment.\n- PLAN: Plan for dangerous wind of equivalent strong tropical\nstorm force.\n- PREPARE: Remaining efforts to protect life and property\nshould be completed as soon as possible. Prepare for\nsignificant wind damage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Significant\n- Some damage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 6-10 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KBRO.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348437-3638981",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.265000000000001,
                                26.539999999999999
                            ],
                            [
                                -97.302000000000007,
                                26.542999999999999
                            ],
                            [
                                -97.363000000000014,
                                26.541999999999998
                            ],
                            [
                                -97.40100000000001,
                                26.541999999999998
                            ],
                            [
                                -97.417000000000016,
                                26.590999999999998
                            ],
                            [
                                -97.447000000000017,
                                26.599999999999998
                            ],
                            [
                                -97.530000000000015,
                                26.600999999999999
                            ],
                            [
                                -97.53400000000002,
                                26.657999999999998
                            ],
                            [
                                -97.550000000000026,
                                26.720999999999997
                            ],
                            [
                                -97.597000000000023,
                                26.826999999999998
                            ],
                            [
                                -97.610000000000028,
                                26.904
                            ],
                            [
                                -97.605000000000032,
                                26.966000000000001
                            ],
                            [
                                -97.580000000000027,
                                27.030000000000001
                            ],
                            [
                                -97.572999900000028,
                                27.076000000000001
                            ],
                            [
                                -97.581000000000031,
                                27.16
                            ],
                            [
                                -97.584999900000028,
                                27.186
                            ],
                            [
                                -97.595000000000027,
                                27.207000000000001
                            ],
                            [
                                -97.632000000000033,
                                27.243000000000002
                            ],
                            [
                                -97.609000000000037,
                                27.243000000000002
                            ],
                            [
                                -97.595000000000041,
                                27.243000000000002
                            ],
                            [
                                -97.541000000000039,
                                27.229000000000003
                            ],
                            [
                                -97.516000000000034,
                                27.232000000000003
                            ],
                            [
                                -97.496000000000038,
                                27.247000000000003
                            ],
                            [
                                -97.470000000000041,
                                27.254000000000005
                            ],
                            [
                                -97.458000000000041,
                                27.263000000000005
                            ],
                            [
                                -97.450000000000045,
                                27.263000000000005
                            ],
                            [
                                -97.423000000000044,
                                27.262000000000004
                            ],
                            [
                                -97.415000000000049,
                                27.278000000000002
                            ],
                            [
                                -97.372000000000043,
                                27.276000000000003
                            ],
                            [
                                -97.366000000000042,
                                27.275000000000002
                            ],
                            [
                                -97.359000000000037,
                                27.278000000000002
                            ],
                            [
                                -97.347000000000037,
                                27.279000000000003
                            ],
                            [
                                -97.355000000000032,
                                26.916000000000004
                            ],
                            [
                                -97.270000000000039,
                                26.563000000000002
                            ],
                            [
                                -97.265000000000001,
                                26.539999999999999
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348437-3638981",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348437-3638981",
                    "areaDesc": "Inland Kenedy",
                    "geocode": {
                        "UGC": [
                            "TXZ251"
                        ],
                        "SAME": [
                            "048261"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ251"
                    ],
                    "references": [],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Extreme",
                    "certainty": "Likely",
                    "urgency": "Immediate",
                    "event": "Hurricane Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Hurricane Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "A Hurricane Warning means hurricane-force winds are expected\nsomewhere within this area within the next 36 hours\n\n* LOCATIONS AFFECTED\n- Sarita\n- King Ranch\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Strong Tropical Storm force\nwind\n- Peak Wind Forecast: 45-60 mph with gusts to 75 mph\n- Window for Tropical Storm force winds: late Saturday\nmorning until early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 58\nto 73 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for dangerous wind of equivalent strong tropical\nstorm force.\n- PREPARE: Remaining efforts to protect life and property\nshould be completed as soon as possible. Prepare for\nsignificant wind damage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Significant\n- Some damage to roofing and siding materials, along with\ndamage to porches, awnings, carports, and sheds. A few\nbuildings experiencing window, door, and garage door\nfailures. Mobile homes damaged, especially if unanchored.\nUnsecured lightweight objects become dangerous projectiles.\n- Several large trees snapped or uprooted, but with greater\nnumbers in places where trees are shallow rooted. Several\nfences and roadway signs blown over.\n- Some roads impassable from large debris, and more within\nurban or heavily wooded places. A few bridges, causeways,\nand access routes impassable.\n- Scattered power and communications outages, but more\nprevalent in areas with above ground lines.\n\n* STORM SURGE\n- No storm surge inundation forecast\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Little to no storm\nsurge flooding\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: There is little to no threat of storm surge flooding.\nRough surf, coastal erosion, and life-threatening rip\ncurrents are possible.\n- PREPARE: Little to no preparations for storm surge flooding\nare needed.\n- ACT: Follow the instructions of local officials. Monitor\nforecasts.\n\n- POTENTIAL IMPACTS: Little to None\n- Little to no potential impacts from storm surge flooding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 6-10 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes\n- http://co.kenedy.tx.us\n- https://www.211texas.org/cms",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "HURRICANE WARNING IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.NEW.KBRO.HU.W.1008.200725T0254Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "EAS",
                            "NWEM"
                        ],
                        "WEAHandling": [
                            "Imminent Threat"
                        ],
                        "CMAMlongtext": [
                            "National Weather Service: A HURRICANE WARNING is in effect for this area for dangerous and damaging winds. This warning is issued up to 36 hours before hazardous conditions begin. Urgently complete efforts to protect life and property. Have food, water, cash, fuel, and medications for 3+ days. FOLLOW INSTRUCTIONS FROM LOCAL OFFICIALS."
                        ],
                        "CMAMtext": [
                            "NWS: HURRICANE WARNING this area. Check media and local authorities."
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348438-3638982",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -98.954999999999998,
                                27.268999999999998
                            ],
                            [
                                -98.953999899999999,
                                26.785999999999998
                            ],
                            [
                                -99.010999999999996,
                                26.674999999999997
                            ],
                            [
                                -99.168999999999997,
                                26.571999999999996
                            ],
                            [
                                -99.177999999999997,
                                26.619999999999994
                            ],
                            [
                                -99.201999999999998,
                                26.662999999999993
                            ],
                            [
                                -99.2099999,
                                26.693999999999992
                            ],
                            [
                                -99.209000000000003,
                                26.724999999999991
                            ],
                            [
                                -99.240000000000009,
                                26.745999999999992
                            ],
                            [
                                -99.243000000000009,
                                26.788999999999991
                            ],
                            [
                                -99.262000000000015,
                                26.815999999999992
                            ],
                            [
                                -99.26900000000002,
                                26.842999999999993
                            ],
                            [
                                -99.280000000000015,
                                26.857999999999993
                            ],
                            [
                                -99.295000000000016,
                                26.864999999999995
                            ],
                            [
                                -99.316999900000013,
                                26.865999999999996
                            ],
                            [
                                -99.328999900000014,
                                26.879999999999995
                            ],
                            [
                                -99.322000000000017,
                                26.906999999999996
                            ],
                            [
                                -99.325000000000017,
                                26.915999999999997
                            ],
                            [
                                -99.379000000000019,
                                26.934999999999995
                            ],
                            [
                                -99.39400000000002,
                                26.959999999999994
                            ],
                            [
                                -99.377000000000024,
                                26.973999999999993
                            ],
                            [
                                -99.378000000000029,
                                26.979999999999993
                            ],
                            [
                                -99.404000000000025,
                                26.996999999999993
                            ],
                            [
                                -99.416000000000025,
                                27.016999999999992
                            ],
                            [
                                -99.432000000000031,
                                27.010999999999992
                            ],
                            [
                                -99.446000000000026,
                                27.022999999999993
                            ],
                            [
                                -99.444000000000031,
                                27.036999999999992
                            ],
                            [
                                -99.452000000000027,
                                27.062999999999992
                            ],
                            [
                                -99.435000000000031,
                                27.077999999999992
                            ],
                            [
                                -99.42900000000003,
                                27.091999999999992
                            ],
                            [
                                -99.441999900000027,
                                27.10799999999999
                            ],
                            [
                                -99.431000000000026,
                                27.127999999999989
                            ],
                            [
                                -99.438999900000027,
                                27.15199999999999
                            ],
                            [
                                -99.430000000000021,
                                27.159999999999989
                            ],
                            [
                                -99.426000000000016,
                                27.175999999999988
                            ],
                            [
                                -99.433000000000021,
                                27.208999999999989
                            ],
                            [
                                -99.444999900000028,
                                27.222999999999988
                            ],
                            [
                                -99.441999900000027,
                                27.249999999999989
                            ],
                            [
                                -99.453000000000031,
                                27.26499999999999
                            ],
                            [
                                -99.371000000000038,
                                27.318999999999988
                            ],
                            [
                                -99.334000000000032,
                                27.272999999999989
                            ],
                            [
                                -98.954999999999998,
                                27.268999999999998
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348438-3638982",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348438-3638982",
                    "areaDesc": "Zapata",
                    "geocode": {
                        "UGC": [
                            "TXZ248"
                        ],
                        "SAME": [
                            "048505"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ248"
                    ],
                    "references": [],
                    "sent": "2020-07-24T21:54:00-05:00",
                    "effective": "2020-07-24T21:54:00-05:00",
                    "onset": "2020-07-24T21:54:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:54PM CDT by NWS Brownsville TX",
                    "description": "A Tropical Storm Warning means tropical storm-force winds are\nexpected somewhere within this area within the next 36 hours\n\n* LOCATIONS AFFECTED\n- Zapata\n- San Ygnacio\n\n* WIND\n- LATEST LOCAL FORECAST: Equivalent Tropical Storm force wind\n- Peak Wind Forecast: 35-45 mph with gusts to 60 mph\n- Window for Tropical Storm force winds: Saturday evening\nuntil early Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 4-8 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for major\nflooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmajor flooding from heavy rain. Evacuations and rescues are\nlikely.\n- PREPARE: Strongly consider protective actions, especially\nif you are in an area vulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction will likely result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Extensive\n- Major rainfall flooding may prompt many evacuations and\nrescues.\n- Rivers and tributaries may rapidly overflow their banks in\nmultiple places. Small streams, creeks, canals, arroyos,\nand ditches may become dangerous rivers. In mountain areas,\ndestructive runoff may run quickly down valleys while\nincreasing susceptibility to rockslides and mudslides.\nFlood control systems and barriers may become stressed.\n- Flood waters can enter many structures within multiple\ncommunities, some structures becoming uninhabitable or\nwashed away. Many places where flood waters may cover\nescape routes. Streets and parking lots become rivers of\nmoving water with underpasses submerged. Driving conditions\nbecome dangerous. Many road and bridge closures with some\nweakened or washed out.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is unfavorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Tornadoes not expected\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Tornadoes are not expected. Showers and thunderstorms\nwith gusty winds may still occur.\n- PREPARE: Little to no preparations needed to protect\nagainst tornadoes at this time. Keep informed of the latest\ntornado situation.\n- ACT: Listen for changes in the forecast.\n\n- POTENTIAL IMPACTS: Little to None\n- Little to no potential impacts from tornadoes.\n\n* FOR MORE INFORMATION:\n- http://ready.gov/hurricanes",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.EXA.KBRO.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "BROTCVBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348420-3638961",
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [
                                    -94.7069999,
                                    29.335000000000001
                                ],
                                [
                                    -95.113,
                                    29.081
                                ],
                                [
                                    -95.119,
                                    29.085999999999999
                                ],
                                [
                                    -95.120000000000005,
                                    29.091999999999999
                                ],
                                [
                                    -95.053000000000011,
                                    29.190999999999999
                                ],
                                [
                                    -95.058000000000007,
                                    29.198999999999998
                                ],
                                [
                                    -94.996000000000009,
                                    29.255999999999997
                                ],
                                [
                                    -94.943000000000012,
                                    29.305999999999997
                                ],
                                [
                                    -94.894000000000005,
                                    29.308999999999997
                                ],
                                [
                                    -94.890000000000001,
                                    29.368999999999996
                                ],
                                [
                                    -94.891000000000005,
                                    29.432999999999996
                                ],
                                [
                                    -94.810000000000002,
                                    29.363999999999997
                                ],
                                [
                                    -94.7069999,
                                    29.335000000000001
                                ]
                            ]
                        ],
                        [
                            [
                                [
                                    -94.371000000000009,
                                    29.553999999999998
                                ],
                                [
                                    -94.501000000000005,
                                    29.504999999999999
                                ],
                                [
                                    -94.609999999999999,
                                    29.460999999999999
                                ],
                                [
                                    -94.679999999999993,
                                    29.424999999999997
                                ],
                                [
                                    -94.714999999999989,
                                    29.395999999999997
                                ],
                                [
                                    -94.730999999999995,
                                    29.368999999999996
                                ],
                                [
                                    -94.744,
                                    29.368999999999996
                                ],
                                [
                                    -94.753,
                                    29.356999999999996
                                ],
                                [
                                    -94.775000000000006,
                                    29.360999999999997
                                ],
                                [
                                    -94.782000000000011,
                                    29.363999999999997
                                ],
                                [
                                    -94.783000000000015,
                                    29.375999999999998
                                ],
                                [
                                    -94.76600000000002,
                                    29.393999999999998
                                ],
                                [
                                    -94.725000000000023,
                                    29.441999999999997
                                ],
                                [
                                    -94.706000000000017,
                                    29.435999999999996
                                ],
                                [
                                    -94.694000000000017,
                                    29.459999999999997
                                ],
                                [
                                    -94.688999900000013,
                                    29.464999999999996
                                ],
                                [
                                    -94.672000000000011,
                                    29.476999999999997
                                ],
                                [
                                    -94.640000000000015,
                                    29.487999999999996
                                ],
                                [
                                    -94.598000000000013,
                                    29.494999999999997
                                ],
                                [
                                    -94.600000000000009,
                                    29.520999999999997
                                ],
                                [
                                    -94.551000000000002,
                                    29.537999999999997
                                ],
                                [
                                    -94.531999999999996,
                                    29.517999999999997
                                ],
                                [
                                    -94.510999999999996,
                                    29.518999999999998
                                ],
                                [
                                    -94.509999999999991,
                                    29.523
                                ],
                                [
                                    -94.472999999999985,
                                    29.556999999999999
                                ],
                                [
                                    -94.459999899999985,
                                    29.561
                                ],
                                [
                                    -94.417999999999992,
                                    29.568999999999999
                                ],
                                [
                                    -94.412999999999997,
                                    29.573
                                ],
                                [
                                    -94.417000000000002,
                                    29.579000000000001
                                ],
                                [
                                    -94.412000000000006,
                                    29.587
                                ],
                                [
                                    -94.419000000000011,
                                    29.588999999999999
                                ],
                                [
                                    -94.410000000000011,
                                    29.596999999999998
                                ],
                                [
                                    -94.373000000000005,
                                    29.596999999999998
                                ],
                                [
                                    -94.371000000000009,
                                    29.553999999999998
                                ]
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348420-3638961",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348420-3638961",
                    "areaDesc": "Galveston Island and Bolivar Peninsula",
                    "geocode": {
                        "UGC": [
                            "TXZ438"
                        ],
                        "SAME": [
                            "048167"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ438"
                    ],
                    "references": [],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "A Tropical Storm Warning means tropical storm-force winds are\nexpected somewhere within this area within the next 36 hours\n\n* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 15-25 mph with gusts to 35 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Wind less than 39 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: The sustained wind should remain less than tropical\nstorm force. Conditions may still be gusty.\n- PREPARE: Listen for any instructions from local officials.\n- ACT: Ensure emergency readiness should the forecast change.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional wind impacts expected. Community\nofficials are now assessing the extent of actual wind\nimpacts accordingly.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for up to 2 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday morning\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has increased from the previous\nassessment.\n- PLAN: Shelter against storm surge flooding greater than 1\nfoot above ground.\n- PREPARE: All flood preparations should be complete. Expect\nflooding of low-lying roads and property.\n- ACT: Stay away from storm surge prone areas. Continue to\nfollow the instructions of local officials.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is unfavorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Tornadoes not expected\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Tornadoes are not expected. Showers and thunderstorms\nwith gusty winds may still occur.\n- PREPARE: Little to no preparations needed to protect\nagainst tornadoes at this time. Keep informed of the latest\ntornado situation.\n- ACT: Listen for changes in the forecast.\n\n- POTENTIAL IMPACTS: Little to None\n- Little to no potential impacts from tornadoes.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.EXA.KHGX.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348418-3638957",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -95.534000000000006,
                                28.829999999999998
                            ],
                            [
                                -95.539000000000001,
                                28.811999999999998
                            ],
                            [
                                -95.635999999999996,
                                28.763999999999999
                            ],
                            [
                                -95.668999999999997,
                                28.765000000000001
                            ],
                            [
                                -95.727999999999994,
                                28.740000000000002
                            ],
                            [
                                -95.751999999999995,
                                28.749000000000002
                            ],
                            [
                                -95.778999999999996,
                                28.749000000000002
                            ],
                            [
                                -95.876999999999995,
                                28.721000000000004
                            ],
                            [
                                -95.989999999999995,
                                28.676000000000002
                            ],
                            [
                                -96.049999999999997,
                                28.656000000000002
                            ],
                            [
                                -96.082999999999998,
                                28.635000000000002
                            ],
                            [
                                -96.162999999999997,
                                28.611000000000001
                            ],
                            [
                                -96.179000000000002,
                                28.591000000000001
                            ],
                            [
                                -96.350999999999999,
                                28.536000000000001
                            ],
                            [
                                -96.323999999999998,
                                28.642000000000003
                            ],
                            [
                                -96.323999999999998,
                                28.676000000000002
                            ],
                            [
                                -96.317999999999998,
                                28.789000000000001
                            ],
                            [
                                -96.078999899999999,
                                28.787000000000003
                            ],
                            [
                                -96.054000000000002,
                                28.809000000000001
                            ],
                            [
                                -96.030000000000001,
                                28.788
                            ],
                            [
                                -96,
                                28.788
                            ],
                            [
                                -95.859999999999999,
                                28.835999999999999
                            ],
                            [
                                -95.742999999999995,
                                28.923999999999999
                            ],
                            [
                                -95.690999999999988,
                                28.965
                            ],
                            [
                                -95.675999999999988,
                                28.963999999999999
                            ],
                            [
                                -95.645999999999987,
                                28.939
                            ],
                            [
                                -95.651999999999987,
                                28.923000000000002
                            ],
                            [
                                -95.642999999999986,
                                28.906000000000002
                            ],
                            [
                                -95.579999999999984,
                                28.860000000000003
                            ],
                            [
                                -95.572999899999985,
                                28.833000000000002
                            ],
                            [
                                -95.534000000000006,
                                28.829999999999998
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348418-3638957",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348418-3638957",
                    "areaDesc": "Coastal Matagorda",
                    "geocode": {
                        "UGC": [
                            "TXZ336"
                        ],
                        "SAME": [
                            "048321"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ336"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345697-3637291",
                            "identifier": "NWS-IDP-PROD-4345697-3637291",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345697-3637290",
                            "identifier": "NWS-IDP-PROD-4345697-3637290",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347709-3638484",
                            "identifier": "NWS-IDP-PROD-4347709-3638484",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347709-3638483",
                            "identifier": "NWS-IDP-PROD-4347709-3638483",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346512-3637765",
                            "identifier": "NWS-IDP-PROD-4346512-3637765",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346870-3637997",
                            "identifier": "NWS-IDP-PROD-4346870-3637997",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347037-3638110",
                            "identifier": "NWS-IDP-PROD-4347037-3638110",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347174-3638176",
                            "identifier": "NWS-IDP-PROD-4347174-3638176",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 20-30 mph with gusts to 35 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Wind less than 39 mph\n- The wind threat has decreased from the previous assessment.\n- PLAN: The sustained wind should remain less than tropical\nstorm force. Conditions may still be gusty.\n- PREPARE: Listen for any instructions from local officials.\n- ACT: Ensure emergency readiness should the forecast change.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional wind impacts expected. Community\nofficials are now assessing the extent of actual wind\nimpacts accordingly.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for 1-3 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday afternoon\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: The threat from storm surge is diminishing as flood\nwaters recede.\n- PREPARE: Heed instructions from local officials when moving\nabout. Do not enter flooded areas.\n- ACT: Exercise safety.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional surge impacts expected. Community\nofficials are now assessing the extent of actual surge\nimpacts accordingly.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 2-4 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plans should still include the potential for a few\ntornadoes.\n- PREPARE: Keep informed should additional weather alerts be\nneeded.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "STORM SURGE WARNING REMAINS IN EFFECT... ...TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348421-3638962",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -95.691000000000003,
                                28.965
                            ],
                            [
                                -95.743000000000009,
                                28.923999999999999
                            ],
                            [
                                -95.860000000000014,
                                28.835999999999999
                            ],
                            [
                                -96.000000000000014,
                                28.788
                            ],
                            [
                                -96.030000000000015,
                                28.788
                            ],
                            [
                                -96.054000000000016,
                                28.809000000000001
                            ],
                            [
                                -96.078999900000014,
                                28.787000000000003
                            ],
                            [
                                -96.318000000000012,
                                28.789000000000001
                            ],
                            [
                                -96.308000000000007,
                                28.964000000000002
                            ],
                            [
                                -95.965000000000003,
                                29.147000000000002
                            ],
                            [
                                -95.874000000000009,
                                29.229000000000003
                            ],
                            [
                                -95.845000000000013,
                                29.205000000000002
                            ],
                            [
                                -95.857000000000014,
                                29.194000000000003
                            ],
                            [
                                -95.837999900000014,
                                29.177000000000003
                            ],
                            [
                                -95.851000000000013,
                                29.152000000000005
                            ],
                            [
                                -95.837999900000014,
                                29.133000000000006
                            ],
                            [
                                -95.846000000000018,
                                29.107000000000006
                            ],
                            [
                                -95.837999900000014,
                                29.095000000000006
                            ],
                            [
                                -95.830000000000013,
                                29.090000000000007
                            ],
                            [
                                -95.806000000000012,
                                29.091000000000008
                            ],
                            [
                                -95.792000000000016,
                                29.07200000000001
                            ],
                            [
                                -95.765000000000015,
                                29.061000000000011
                            ],
                            [
                                -95.785000000000011,
                                29.039000000000012
                            ],
                            [
                                -95.77600000000001,
                                29.018000000000011
                            ],
                            [
                                -95.785000000000011,
                                29.009000000000011
                            ],
                            [
                                -95.772000000000006,
                                29.006000000000011
                            ],
                            [
                                -95.777000000000001,
                                28.997000000000011
                            ],
                            [
                                -95.768000000000001,
                                28.99100000000001
                            ],
                            [
                                -95.768000000000001,
                                28.97000000000001
                            ],
                            [
                                -95.691000000000003,
                                28.965
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348421-3638962",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348421-3638962",
                    "areaDesc": "Inland Matagorda",
                    "geocode": {
                        "UGC": [
                            "TXZ236"
                        ],
                        "SAME": [
                            "048321"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ236"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346872-3637999",
                            "identifier": "NWS-IDP-PROD-4346872-3637999",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345693-3637285",
                            "identifier": "NWS-IDP-PROD-4345693-3637285",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345693-3637284",
                            "identifier": "NWS-IDP-PROD-4345693-3637284",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347041-3638114",
                            "identifier": "NWS-IDP-PROD-4347041-3638114",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346513-3637766",
                            "identifier": "NWS-IDP-PROD-4346513-3637766",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347706-3638479",
                            "identifier": "NWS-IDP-PROD-4347706-3638479",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347184-3638186",
                            "identifier": "NWS-IDP-PROD-4347184-3638186",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 15-25 mph with gusts to 30 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Wind less than 39 mph\n- The wind threat has decreased from the previous assessment.\n- PLAN: The sustained wind should remain less than tropical\nstorm force. Conditions may still be gusty.\n- PREPARE: Listen for any instructions from local officials.\n- ACT: Ensure emergency readiness should the forecast change.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional wind impacts expected. Community\nofficials are now assessing the extent of actual wind\nimpacts accordingly.\n\n* STORM SURGE\n- No storm surge inundation forecast\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Little to no storm\nsurge flooding\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: There is little to no threat of storm surge flooding.\nRough surf, coastal erosion, and life-threatening rip\ncurrents are possible.\n- PREPARE: Little to no preparations for storm surge flooding\nare needed.\n- ACT: Follow the instructions of local officials. Monitor\nforecasts.\n\n- POTENTIAL IMPACTS: Little to None\n- Little to no potential impacts from storm surge flooding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 2-4 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plans should still include the potential for a few\ntornadoes.\n- PREPARE: Keep informed should additional weather alerts be\nneeded.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348419-3638959",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -95.504999999999995,
                                28.826000000000001
                            ],
                            [
                                -95.521000000000001,
                                28.806000000000001
                            ],
                            [
                                -96.376000000000005,
                                28.374000000000002
                            ],
                            [
                                -96.385000000000005,
                                28.396000000000001
                            ],
                            [
                                -96.350999999999999,
                                28.536000000000001
                            ],
                            [
                                -96.179000000000002,
                                28.591000000000001
                            ],
                            [
                                -96.162999999999997,
                                28.611000000000001
                            ],
                            [
                                -96.082999999999998,
                                28.635000000000002
                            ],
                            [
                                -96.049999999999997,
                                28.656000000000002
                            ],
                            [
                                -95.989999999999995,
                                28.676000000000002
                            ],
                            [
                                -95.876999999999995,
                                28.721000000000004
                            ],
                            [
                                -95.778999999999996,
                                28.749000000000002
                            ],
                            [
                                -95.751999999999995,
                                28.749000000000002
                            ],
                            [
                                -95.727999999999994,
                                28.740000000000002
                            ],
                            [
                                -95.668999999999997,
                                28.765000000000001
                            ],
                            [
                                -95.635999999999996,
                                28.763999999999999
                            ],
                            [
                                -95.539000000000001,
                                28.811999999999998
                            ],
                            [
                                -95.534000000000006,
                                28.829999999999998
                            ],
                            [
                                -95.50800000000001,
                                28.837
                            ],
                            [
                                -95.504999999999995,
                                28.826000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348419-3638959",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348419-3638959",
                    "areaDesc": "Matagorda Islands",
                    "geocode": {
                        "UGC": [
                            "TXZ436"
                        ],
                        "SAME": [
                            "048321"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ436"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347045-3638118",
                            "identifier": "NWS-IDP-PROD-4347045-3638118",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346518-3637771",
                            "identifier": "NWS-IDP-PROD-4346518-3637771",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347705-3638478",
                            "identifier": "NWS-IDP-PROD-4347705-3638478",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347705-3638477",
                            "identifier": "NWS-IDP-PROD-4347705-3638477",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345701-3637296",
                            "identifier": "NWS-IDP-PROD-4345701-3637296",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345701-3637295",
                            "identifier": "NWS-IDP-PROD-4345701-3637295",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346877-3638004",
                            "identifier": "NWS-IDP-PROD-4346877-3638004",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347183-3638185",
                            "identifier": "NWS-IDP-PROD-4347183-3638185",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 25-35 mph with gusts to 45 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Life-threatening storm surge possible\n- Peak Storm Surge Inundation: The potential for 3-5 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday afternoon\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 3 feet above ground\n- The storm surge threat has increased from the previous\nassessment.\n- PLAN: Shelter against life-threatening storm surge of\ngreater than 3 feet above ground.\n- PREPARE: Flood preparations and ordered evacuations should\nbe complete. Evacuees should be in shelters well away from\nstorm surge flooding.\n- ACT: Remain sheltered in a safe location. Do not venture\noutside.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "STORM SURGE WARNING REMAINS IN EFFECT... ...TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348416-3638955",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -96.308000000000007,
                                28.963999999999999
                            ],
                            [
                                -96.318000000000012,
                                28.788999999999998
                            ],
                            [
                                -96.376000000000019,
                                28.854999999999997
                            ],
                            [
                                -96.424000000000021,
                                28.842999999999996
                            ],
                            [
                                -96.464000000000027,
                                28.840999999999998
                            ],
                            [
                                -96.522000000000034,
                                28.822999999999997
                            ],
                            [
                                -96.54400000000004,
                                28.821999999999996
                            ],
                            [
                                -96.697999900000042,
                                28.778999999999996
                            ],
                            [
                                -96.694999900000042,
                                28.792999999999996
                            ],
                            [
                                -96.706000000000046,
                                28.796999999999997
                            ],
                            [
                                -96.706000000000046,
                                28.814999999999998
                            ],
                            [
                                -96.723000000000042,
                                28.821999999999999
                            ],
                            [
                                -96.712000000000046,
                                28.831
                            ],
                            [
                                -96.717000000000041,
                                28.837
                            ],
                            [
                                -96.712999900000042,
                                28.844000000000001
                            ],
                            [
                                -96.703000000000046,
                                28.850000000000001
                            ],
                            [
                                -96.712999900000042,
                                28.853000000000002
                            ],
                            [
                                -96.729000000000042,
                                28.871000000000002
                            ],
                            [
                                -96.733000000000047,
                                28.889000000000003
                            ],
                            [
                                -96.760000000000048,
                                28.898000000000003
                            ],
                            [
                                -96.776000000000053,
                                28.916000000000004
                            ],
                            [
                                -96.791000000000054,
                                28.918000000000003
                            ],
                            [
                                -96.807000000000059,
                                28.956000000000003
                            ],
                            [
                                -96.806000000000054,
                                28.973000000000003
                            ],
                            [
                                -96.831999900000056,
                                29.021000000000001
                            ],
                            [
                                -96.938999900000056,
                                29.063000000000002
                            ],
                            [
                                -96.658000000000058,
                                29.264000000000003
                            ],
                            [
                                -96.640000000000057,
                                29.248000000000005
                            ],
                            [
                                -96.308000000000007,
                                28.963999999999999
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348416-3638955",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348416-3638955",
                    "areaDesc": "Inland Jackson",
                    "geocode": {
                        "UGC": [
                            "TXZ235"
                        ],
                        "SAME": [
                            "048239"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ235"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347704-3638476",
                            "identifier": "NWS-IDP-PROD-4347704-3638476",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347042-3638115",
                            "identifier": "NWS-IDP-PROD-4347042-3638115",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346874-3638001",
                            "identifier": "NWS-IDP-PROD-4346874-3638001",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346515-3637768",
                            "identifier": "NWS-IDP-PROD-4346515-3637768",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347181-3638183",
                            "identifier": "NWS-IDP-PROD-4347181-3638183",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345689-3637279",
                            "identifier": "NWS-IDP-PROD-4345689-3637279",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345689-3637278",
                            "identifier": "NWS-IDP-PROD-4345689-3637278",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 15-25 mph with gusts to 30 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Wind less than 39 mph\n- The wind threat has decreased from the previous assessment.\n- PLAN: The sustained wind should remain less than tropical\nstorm force. Conditions may still be gusty.\n- PREPARE: Listen for any instructions from local officials.\n- ACT: Ensure emergency readiness should the forecast change.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional wind impacts expected. Community\nofficials are now assessing the extent of actual wind\nimpacts accordingly.\n\n* STORM SURGE\n- No storm surge inundation forecast\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Little to no storm\nsurge flooding\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: There is little to no threat of storm surge flooding.\nRough surf, coastal erosion, and life-threatening rip\ncurrents are possible.\n- PREPARE: Little to no preparations for storm surge flooding\nare needed.\n- ACT: Follow the instructions of local officials. Monitor\nforecasts.\n\n- POTENTIAL IMPACTS: Little to None\n- Little to no potential impacts from storm surge flooding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 2-4 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plans should still include the potential for a few\ntornadoes.\n- PREPARE: Keep informed should additional weather alerts be\nneeded.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348418-3638958",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -95.676000000000002,
                                28.963999999999999
                            ],
                            [
                                -95.646000000000001,
                                28.939
                            ],
                            [
                                -95.652000000000001,
                                28.923000000000002
                            ],
                            [
                                -95.643000000000001,
                                28.906000000000002
                            ],
                            [
                                -95.579999999999998,
                                28.860000000000003
                            ],
                            [
                                -95.572999899999999,
                                28.833000000000002
                            ],
                            [
                                -95.534000000000006,
                                28.830000000000002
                            ],
                            [
                                -95.539000000000001,
                                28.812000000000001
                            ],
                            [
                                -95.635999999999996,
                                28.764000000000003
                            ],
                            [
                                -95.668999999999997,
                                28.765000000000004
                            ],
                            [
                                -95.727999999999994,
                                28.740000000000006
                            ],
                            [
                                -95.751999999999995,
                                28.749000000000006
                            ],
                            [
                                -95.778999999999996,
                                28.749000000000006
                            ],
                            [
                                -95.876999999999995,
                                28.721000000000007
                            ],
                            [
                                -95.989999999999995,
                                28.676000000000005
                            ],
                            [
                                -96.049999999999997,
                                28.656000000000006
                            ],
                            [
                                -96.082999999999998,
                                28.635000000000005
                            ],
                            [
                                -96.162999999999997,
                                28.611000000000004
                            ],
                            [
                                -96.179000000000002,
                                28.591000000000005
                            ],
                            [
                                -96.350999999999999,
                                28.536000000000005
                            ],
                            [
                                -96.323999999999998,
                                28.642000000000007
                            ],
                            [
                                -96.323999999999998,
                                28.676000000000005
                            ],
                            [
                                -96.317999999999998,
                                28.789000000000005
                            ],
                            [
                                -96.078999899999999,
                                28.787000000000006
                            ],
                            [
                                -96.054000000000002,
                                28.809000000000005
                            ],
                            [
                                -96.030000000000001,
                                28.788000000000004
                            ],
                            [
                                -96,
                                28.788000000000004
                            ],
                            [
                                -95.859999999999999,
                                28.836000000000002
                            ],
                            [
                                -95.742999999999995,
                                28.924000000000003
                            ],
                            [
                                -95.690999999999988,
                                28.965000000000003
                            ],
                            [
                                -95.676000000000002,
                                28.963999999999999
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348418-3638958",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348418-3638958",
                    "areaDesc": "Coastal Matagorda",
                    "geocode": {
                        "UGC": [
                            "TXZ336"
                        ],
                        "SAME": [
                            "048321"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ336"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345697-3637291",
                            "identifier": "NWS-IDP-PROD-4345697-3637291",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345697-3637290",
                            "identifier": "NWS-IDP-PROD-4345697-3637290",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347709-3638484",
                            "identifier": "NWS-IDP-PROD-4347709-3638484",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347709-3638483",
                            "identifier": "NWS-IDP-PROD-4347709-3638483",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346512-3637765",
                            "identifier": "NWS-IDP-PROD-4346512-3637765",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346870-3637997",
                            "identifier": "NWS-IDP-PROD-4346870-3637997",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347037-3638110",
                            "identifier": "NWS-IDP-PROD-4347037-3638110",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347174-3638176",
                            "identifier": "NWS-IDP-PROD-4347174-3638176",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Extreme",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "event": "Storm Surge Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Storm Surge Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 20-30 mph with gusts to 35 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Wind less than 39 mph\n- The wind threat has decreased from the previous assessment.\n- PLAN: The sustained wind should remain less than tropical\nstorm force. Conditions may still be gusty.\n- PREPARE: Listen for any instructions from local officials.\n- ACT: Ensure emergency readiness should the forecast change.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional wind impacts expected. Community\nofficials are now assessing the extent of actual wind\nimpacts accordingly.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for 1-3 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday afternoon\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: The threat from storm surge is diminishing as flood\nwaters recede.\n- PREPARE: Heed instructions from local officials when moving\nabout. Do not enter flooded areas.\n- ACT: Exercise safety.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional surge impacts expected. Community\nofficials are now assessing the extent of actual surge\nimpacts accordingly.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 2-4 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plans should still include the potential for a few\ntornadoes.\n- PREPARE: Keep informed should additional weather alerts be\nneeded.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "STORM SURGE WARNING REMAINS IN EFFECT... ...TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.SS.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "EAS",
                            "NWEM",
                            "CMAS"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348419-3638960",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -95.504999999999995,
                                28.826000000000001
                            ],
                            [
                                -95.521000000000001,
                                28.806000000000001
                            ],
                            [
                                -96.376000000000005,
                                28.374000000000002
                            ],
                            [
                                -96.385000000000005,
                                28.396000000000001
                            ],
                            [
                                -96.350999999999999,
                                28.536000000000001
                            ],
                            [
                                -96.179000000000002,
                                28.591000000000001
                            ],
                            [
                                -96.162999999999997,
                                28.611000000000001
                            ],
                            [
                                -96.082999999999998,
                                28.635000000000002
                            ],
                            [
                                -96.049999999999997,
                                28.656000000000002
                            ],
                            [
                                -95.989999999999995,
                                28.676000000000002
                            ],
                            [
                                -95.876999999999995,
                                28.721000000000004
                            ],
                            [
                                -95.778999999999996,
                                28.749000000000002
                            ],
                            [
                                -95.751999999999995,
                                28.749000000000002
                            ],
                            [
                                -95.727999999999994,
                                28.740000000000002
                            ],
                            [
                                -95.668999999999997,
                                28.765000000000001
                            ],
                            [
                                -95.635999999999996,
                                28.763999999999999
                            ],
                            [
                                -95.539000000000001,
                                28.811999999999998
                            ],
                            [
                                -95.534000000000006,
                                28.829999999999998
                            ],
                            [
                                -95.50800000000001,
                                28.837
                            ],
                            [
                                -95.504999999999995,
                                28.826000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348419-3638960",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348419-3638960",
                    "areaDesc": "Matagorda Islands",
                    "geocode": {
                        "UGC": [
                            "TXZ436"
                        ],
                        "SAME": [
                            "048321"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ436"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347045-3638118",
                            "identifier": "NWS-IDP-PROD-4347045-3638118",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346518-3637771",
                            "identifier": "NWS-IDP-PROD-4346518-3637771",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347705-3638478",
                            "identifier": "NWS-IDP-PROD-4347705-3638478",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347705-3638477",
                            "identifier": "NWS-IDP-PROD-4347705-3638477",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345701-3637296",
                            "identifier": "NWS-IDP-PROD-4345701-3637296",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345701-3637295",
                            "identifier": "NWS-IDP-PROD-4345701-3637295",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346877-3638004",
                            "identifier": "NWS-IDP-PROD-4346877-3638004",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347183-3638185",
                            "identifier": "NWS-IDP-PROD-4347183-3638185",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Extreme",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "event": "Storm Surge Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Storm Surge Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 25-35 mph with gusts to 45 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for wind 39\nto 57 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plan for hazardous wind of equivalent tropical storm\nforce.\n- PREPARE: Remaining efforts to protect property should be\ncompleted as soon as possible. Prepare for limited wind\ndamage.\n- ACT: Move to safe shelter before the wind becomes hazardous.\n\n- POTENTIAL IMPACTS: Limited\n- Damage to porches, awnings, carports, sheds, and unanchored\nmobile homes. Unsecured lightweight objects blown about.\n- Many large tree limbs broken off. A few trees snapped or\nuprooted, but with greater numbers in places where trees\nare shallow rooted. Some fences and roadway signs blown\nover.\n- A few roads impassable from debris, particularly within\nurban or heavily wooded places. Hazardous driving\nconditions on bridges and other elevated roadways.\n- Scattered power and communications outages.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Life-threatening storm surge possible\n- Peak Storm Surge Inundation: The potential for 3-5 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday afternoon\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 3 feet above ground\n- The storm surge threat has increased from the previous\nassessment.\n- PLAN: Shelter against life-threatening storm surge of\ngreater than 3 feet above ground.\n- PREPARE: Flood preparations and ordered evacuations should\nbe complete. Evacuees should be in shelters well away from\nstorm surge flooding.\n- ACT: Remain sheltered in a safe location. Do not venture\noutside.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Emergency plans should include the potential for a\nfew tornadoes.\n- PREPARE: If your shelter is particularly vulnerable to\ntornadoes, prepare to relocate to safe shelter before\nhazardous weather arrives.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "STORM SURGE WARNING REMAINS IN EFFECT... ...TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.SS.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "EAS",
                            "NWEM",
                            "CMAS"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348423-3638964",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -96.317999999999998,
                                28.789000000000001
                            ],
                            [
                                -96.323999999999998,
                                28.676000000000002
                            ],
                            [
                                -96.390999999999991,
                                28.675000000000001
                            ],
                            [
                                -96.395999999999987,
                                28.68
                            ],
                            [
                                -96.389999999999986,
                                28.690999999999999
                            ],
                            [
                                -96.391999999999982,
                                28.701999999999998
                            ],
                            [
                                -96.382999999999981,
                                28.706999999999997
                            ],
                            [
                                -96.393999999999977,
                                28.709999999999997
                            ],
                            [
                                -96.387999999999977,
                                28.715999999999998
                            ],
                            [
                                -96.389999999999972,
                                28.728999999999999
                            ],
                            [
                                -96.404999999999973,
                                28.736999999999998
                            ],
                            [
                                -96.421999999999969,
                                28.718999999999998
                            ],
                            [
                                -96.432999999999964,
                                28.716999999999999
                            ],
                            [
                                -96.428999999999959,
                                28.739999999999998
                            ],
                            [
                                -96.441999899999956,
                                28.742999999999999
                            ],
                            [
                                -96.44399999999996,
                                28.75
                            ],
                            [
                                -96.45299999999996,
                                28.756
                            ],
                            [
                                -96.44999999999996,
                                28.739000000000001
                            ],
                            [
                                -96.435999999999964,
                                28.738
                            ],
                            [
                                -96.439999999999969,
                                28.719000000000001
                            ],
                            [
                                -96.428999999999974,
                                28.707000000000001
                            ],
                            [
                                -96.427999999999969,
                                28.704000000000001
                            ],
                            [
                                -96.467999999999975,
                                28.702999999999999
                            ],
                            [
                                -96.476999999999975,
                                28.702999999999999
                            ],
                            [
                                -96.47499999999998,
                                28.707000000000001
                            ],
                            [
                                -96.528999999999982,
                                28.706
                            ],
                            [
                                -96.552999999999983,
                                28.704999999999998
                            ],
                            [
                                -96.562999999999988,
                                28.704999999999998
                            ],
                            [
                                -96.573999999999984,
                                28.704999999999998
                            ],
                            [
                                -96.579999999999984,
                                28.696999999999999
                            ],
                            [
                                -96.577999999999989,
                                28.707000000000001
                            ],
                            [
                                -96.586999999999989,
                                28.725000000000001
                            ],
                            [
                                -96.644999999999996,
                                28.711000000000002
                            ],
                            [
                                -96.650999999999996,
                                28.723000000000003
                            ],
                            [
                                -96.658999999999992,
                                28.720000000000002
                            ],
                            [
                                -96.667999999999992,
                                28.737000000000002
                            ],
                            [
                                -96.663999999999987,
                                28.745000000000001
                            ],
                            [
                                -96.671999999999983,
                                28.752000000000002
                            ],
                            [
                                -96.669999999999987,
                                28.761000000000003
                            ],
                            [
                                -96.685999999999993,
                                28.764000000000003
                            ],
                            [
                                -96.685999999999993,
                                28.771000000000004
                            ],
                            [
                                -96.697999899999999,
                                28.776000000000003
                            ],
                            [
                                -96.697999899999999,
                                28.779000000000003
                            ],
                            [
                                -96.543999999999997,
                                28.822000000000003
                            ],
                            [
                                -96.521999999999991,
                                28.823000000000004
                            ],
                            [
                                -96.463999999999984,
                                28.841000000000005
                            ],
                            [
                                -96.423999999999978,
                                28.843000000000004
                            ],
                            [
                                -96.375999999999976,
                                28.855000000000004
                            ],
                            [
                                -96.317999999999998,
                                28.789000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348423-3638964",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348423-3638964",
                    "areaDesc": "Coastal Jackson",
                    "geocode": {
                        "UGC": [
                            "TXZ335"
                        ],
                        "SAME": [
                            "048239"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ335"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347039-3638112",
                            "identifier": "NWS-IDP-PROD-4347039-3638112",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346878-3638005",
                            "identifier": "NWS-IDP-PROD-4346878-3638005",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347179-3638181",
                            "identifier": "NWS-IDP-PROD-4347179-3638181",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345688-3637277",
                            "identifier": "NWS-IDP-PROD-4345688-3637277",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345688-3637276",
                            "identifier": "NWS-IDP-PROD-4345688-3637276",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347707-3638481",
                            "identifier": "NWS-IDP-PROD-4347707-3638481",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347707-3638480",
                            "identifier": "NWS-IDP-PROD-4347707-3638480",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346506-3637759",
                            "identifier": "NWS-IDP-PROD-4346506-3637759",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 20-30 mph with gusts to 35 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Wind less than 39 mph\n- The wind threat has decreased from the previous assessment.\n- PLAN: The sustained wind should remain less than tropical\nstorm force. Conditions may still be gusty.\n- PREPARE: Listen for any instructions from local officials.\n- ACT: Ensure emergency readiness should the forecast change.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional wind impacts expected. Community\nofficials are now assessing the extent of actual wind\nimpacts accordingly.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Life-threatening storm surge possible\n- Peak Storm Surge Inundation: The potential for 2-4 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday afternoon\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 3 feet above ground\n- The storm surge threat has increased from the previous\nassessment.\n- PLAN: Shelter against life-threatening storm surge of\ngreater than 3 feet above ground.\n- PREPARE: Flood preparations and ordered evacuations should\nbe complete. Evacuees should be in shelters well away from\nstorm surge flooding.\n- ACT: Remain sheltered in a safe location. Do not venture\noutside.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 2-4 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plans should still include the potential for a few\ntornadoes.\n- PREPARE: Keep informed should additional weather alerts be\nneeded.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "STORM SURGE WARNING REMAINS IN EFFECT... ...TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348417-3638956",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -95.134,
                                29.314
                            ],
                            [
                                -95.058000000000007,
                                29.199000000000002
                            ],
                            [
                                -95.084000000000003,
                                29.184000000000001
                            ],
                            [
                                -95.096000000000004,
                                29.176000000000002
                            ],
                            [
                                -95.113,
                                29.172000000000001
                            ],
                            [
                                -95.120000000000005,
                                29.172000000000001
                            ],
                            [
                                -95.106999999999999,
                                29.184000000000001
                            ],
                            [
                                -95.111999999999995,
                                29.195
                            ],
                            [
                                -95.137999999999991,
                                29.190000000000001
                            ],
                            [
                                -95.148999999999987,
                                29.183
                            ],
                            [
                                -95.151999999999987,
                                29.152000000000001
                            ],
                            [
                                -95.155999999999992,
                                29.144000000000002
                            ],
                            [
                                -95.157999999999987,
                                29.142000000000003
                            ],
                            [
                                -95.200999899999985,
                                29.106000000000002
                            ],
                            [
                                -95.205999999999989,
                                29.082000000000001
                            ],
                            [
                                -95.22999999999999,
                                29.036999999999999
                            ],
                            [
                                -95.233999999999995,
                                29.018000000000001
                            ],
                            [
                                -95.262,
                                28.986000000000001
                            ],
                            [
                                -95.283000000000001,
                                28.971
                            ],
                            [
                                -95.307000000000002,
                                28.943999999999999
                            ],
                            [
                                -95.322000000000003,
                                28.930999999999997
                            ],
                            [
                                -95.388000000000005,
                                28.895999999999997
                            ],
                            [
                                -95.399000000000001,
                                28.899999999999999
                            ],
                            [
                                -95.445999999999998,
                                28.870999999999999
                            ],
                            [
                                -95.488,
                                28.857999999999997
                            ],
                            [
                                -95.531000000000006,
                                28.833999999999996
                            ],
                            [
                                -95.534000000000006,
                                28.829999999999995
                            ],
                            [
                                -95.572999899999999,
                                28.832999999999995
                            ],
                            [
                                -95.579999999999998,
                                28.859999999999996
                            ],
                            [
                                -95.643000000000001,
                                28.905999999999995
                            ],
                            [
                                -95.652000000000001,
                                28.922999999999995
                            ],
                            [
                                -95.646000000000001,
                                28.938999999999993
                            ],
                            [
                                -95.676000000000002,
                                28.963999999999992
                            ],
                            [
                                -95.691000000000003,
                                28.964999999999993
                            ],
                            [
                                -95.653999999999996,
                                28.992999999999991
                            ],
                            [
                                -95.625999999999991,
                                29.007999999999992
                            ],
                            [
                                -95.549999999999997,
                                29.013999999999992
                            ],
                            [
                                -95.322000000000003,
                                29.212999999999994
                            ],
                            [
                                -95.290000000000006,
                                29.291999999999994
                            ],
                            [
                                -95.259,
                                29.320999999999994
                            ],
                            [
                                -95.165999999999997,
                                29.314999999999994
                            ],
                            [
                                -95.134,
                                29.314
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348417-3638956",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348417-3638956",
                    "areaDesc": "Coastal Brazoria",
                    "geocode": {
                        "UGC": [
                            "TXZ337"
                        ],
                        "SAME": [
                            "048039"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ337"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347703-3638475",
                            "identifier": "NWS-IDP-PROD-4347703-3638475",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347176-3638178",
                            "identifier": "NWS-IDP-PROD-4347176-3638178",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346879-3638006",
                            "identifier": "NWS-IDP-PROD-4346879-3638006",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346511-3637764",
                            "identifier": "NWS-IDP-PROD-4346511-3637764",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347035-3638108",
                            "identifier": "NWS-IDP-PROD-4347035-3638108",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345695-3637288",
                            "identifier": "NWS-IDP-PROD-4345695-3637288",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345695-3637287",
                            "identifier": "NWS-IDP-PROD-4345695-3637287",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 15-25 mph with gusts to 30 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Wind less than 39 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: The sustained wind should remain less than tropical\nstorm force. Conditions may still be gusty.\n- PREPARE: Listen for any instructions from local officials.\n- ACT: Ensure emergency readiness should the forecast change.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional wind impacts expected. Community\nofficials are now assessing the extent of actual wind\nimpacts accordingly.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for 1-3 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday afternoon\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Shelter against storm surge flooding greater than 1\nfoot above ground.\n- PREPARE: All flood preparations should be complete. Expect\nflooding of low-lying roads and property.\n- ACT: Stay away from storm surge prone areas. Continue to\nfollow the instructions of local officials.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 2-4 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plans should still include the potential for a few\ntornadoes.\n- PREPARE: Keep informed should additional weather alerts be\nneeded.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348423-3638965",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -96.317999999999998,
                                28.789000000000001
                            ],
                            [
                                -96.323999999999998,
                                28.676000000000002
                            ],
                            [
                                -96.390999999999991,
                                28.675000000000001
                            ],
                            [
                                -96.395999999999987,
                                28.68
                            ],
                            [
                                -96.389999999999986,
                                28.690999999999999
                            ],
                            [
                                -96.391999999999982,
                                28.701999999999998
                            ],
                            [
                                -96.382999999999981,
                                28.706999999999997
                            ],
                            [
                                -96.393999999999977,
                                28.709999999999997
                            ],
                            [
                                -96.387999999999977,
                                28.715999999999998
                            ],
                            [
                                -96.389999999999972,
                                28.728999999999999
                            ],
                            [
                                -96.404999999999973,
                                28.736999999999998
                            ],
                            [
                                -96.421999999999969,
                                28.718999999999998
                            ],
                            [
                                -96.432999999999964,
                                28.716999999999999
                            ],
                            [
                                -96.428999999999959,
                                28.739999999999998
                            ],
                            [
                                -96.441999899999956,
                                28.742999999999999
                            ],
                            [
                                -96.44399999999996,
                                28.75
                            ],
                            [
                                -96.45299999999996,
                                28.756
                            ],
                            [
                                -96.44999999999996,
                                28.739000000000001
                            ],
                            [
                                -96.435999999999964,
                                28.738
                            ],
                            [
                                -96.439999999999969,
                                28.719000000000001
                            ],
                            [
                                -96.428999999999974,
                                28.707000000000001
                            ],
                            [
                                -96.427999999999969,
                                28.704000000000001
                            ],
                            [
                                -96.467999999999975,
                                28.702999999999999
                            ],
                            [
                                -96.476999999999975,
                                28.702999999999999
                            ],
                            [
                                -96.47499999999998,
                                28.707000000000001
                            ],
                            [
                                -96.528999999999982,
                                28.706
                            ],
                            [
                                -96.552999999999983,
                                28.704999999999998
                            ],
                            [
                                -96.562999999999988,
                                28.704999999999998
                            ],
                            [
                                -96.573999999999984,
                                28.704999999999998
                            ],
                            [
                                -96.579999999999984,
                                28.696999999999999
                            ],
                            [
                                -96.577999999999989,
                                28.707000000000001
                            ],
                            [
                                -96.586999999999989,
                                28.725000000000001
                            ],
                            [
                                -96.644999999999996,
                                28.711000000000002
                            ],
                            [
                                -96.650999999999996,
                                28.723000000000003
                            ],
                            [
                                -96.658999999999992,
                                28.720000000000002
                            ],
                            [
                                -96.667999999999992,
                                28.737000000000002
                            ],
                            [
                                -96.663999999999987,
                                28.745000000000001
                            ],
                            [
                                -96.671999999999983,
                                28.752000000000002
                            ],
                            [
                                -96.669999999999987,
                                28.761000000000003
                            ],
                            [
                                -96.685999999999993,
                                28.764000000000003
                            ],
                            [
                                -96.685999999999993,
                                28.771000000000004
                            ],
                            [
                                -96.697999899999999,
                                28.776000000000003
                            ],
                            [
                                -96.697999899999999,
                                28.779000000000003
                            ],
                            [
                                -96.543999999999997,
                                28.822000000000003
                            ],
                            [
                                -96.521999999999991,
                                28.823000000000004
                            ],
                            [
                                -96.463999999999984,
                                28.841000000000005
                            ],
                            [
                                -96.423999999999978,
                                28.843000000000004
                            ],
                            [
                                -96.375999999999976,
                                28.855000000000004
                            ],
                            [
                                -96.317999999999998,
                                28.789000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348423-3638965",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348423-3638965",
                    "areaDesc": "Coastal Jackson",
                    "geocode": {
                        "UGC": [
                            "TXZ335"
                        ],
                        "SAME": [
                            "048239"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ335"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347039-3638112",
                            "identifier": "NWS-IDP-PROD-4347039-3638112",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346878-3638005",
                            "identifier": "NWS-IDP-PROD-4346878-3638005",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347179-3638181",
                            "identifier": "NWS-IDP-PROD-4347179-3638181",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345688-3637277",
                            "identifier": "NWS-IDP-PROD-4345688-3637277",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345688-3637276",
                            "identifier": "NWS-IDP-PROD-4345688-3637276",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347707-3638481",
                            "identifier": "NWS-IDP-PROD-4347707-3638481",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347707-3638480",
                            "identifier": "NWS-IDP-PROD-4347707-3638480",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346506-3637759",
                            "identifier": "NWS-IDP-PROD-4346506-3637759",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Extreme",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "event": "Storm Surge Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Storm Surge Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 20-30 mph with gusts to 35 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Wind less than 39 mph\n- The wind threat has decreased from the previous assessment.\n- PLAN: The sustained wind should remain less than tropical\nstorm force. Conditions may still be gusty.\n- PREPARE: Listen for any instructions from local officials.\n- ACT: Ensure emergency readiness should the forecast change.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional wind impacts expected. Community\nofficials are now assessing the extent of actual wind\nimpacts accordingly.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Life-threatening storm surge possible\n- Peak Storm Surge Inundation: The potential for 2-4 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday afternoon\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 3 feet above ground\n- The storm surge threat has increased from the previous\nassessment.\n- PLAN: Shelter against life-threatening storm surge of\ngreater than 3 feet above ground.\n- PREPARE: Flood preparations and ordered evacuations should\nbe complete. Evacuees should be in shelters well away from\nstorm surge flooding.\n- ACT: Remain sheltered in a safe location. Do not venture\noutside.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 2-4 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plans should still include the potential for a few\ntornadoes.\n- PREPARE: Keep informed should additional weather alerts be\nneeded.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "STORM SURGE WARNING REMAINS IN EFFECT... ...TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.SS.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "EAS",
                            "NWEM",
                            "CMAS"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348422-3638963",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -95.504999999999995,
                                28.826000000000001
                            ],
                            [
                                -95.507999999999996,
                                28.837
                            ],
                            [
                                -95.533999999999992,
                                28.829999999999998
                            ],
                            [
                                -95.530999999999992,
                                28.834
                            ],
                            [
                                -95.487999999999985,
                                28.858000000000001
                            ],
                            [
                                -95.445999999999984,
                                28.871000000000002
                            ],
                            [
                                -95.398999999999987,
                                28.900000000000002
                            ],
                            [
                                -95.387999999999991,
                                28.896000000000001
                            ],
                            [
                                -95.321999999999989,
                                28.931000000000001
                            ],
                            [
                                -95.306999999999988,
                                28.944000000000003
                            ],
                            [
                                -95.282999999999987,
                                28.971000000000004
                            ],
                            [
                                -95.261999999999986,
                                28.986000000000004
                            ],
                            [
                                -95.23399999999998,
                                29.018000000000004
                            ],
                            [
                                -95.229999999999976,
                                29.037000000000003
                            ],
                            [
                                -95.205999999999975,
                                29.082000000000004
                            ],
                            [
                                -95.200999899999971,
                                29.106000000000005
                            ],
                            [
                                -95.157999999999973,
                                29.142000000000007
                            ],
                            [
                                -95.117999999999967,
                                29.068000000000005
                            ],
                            [
                                -95.261999999999972,
                                28.969000000000005
                            ],
                            [
                                -95.295999999999978,
                                28.935000000000006
                            ],
                            [
                                -95.334999899999971,
                                28.915000000000006
                            ],
                            [
                                -95.379999999999967,
                                28.876000000000005
                            ],
                            [
                                -95.383999999999972,
                                28.866000000000003
                            ],
                            [
                                -95.396999999999977,
                                28.862000000000002
                            ],
                            [
                                -95.432999999999979,
                                28.860000000000003
                            ],
                            [
                                -95.440999999999974,
                                28.857000000000003
                            ],
                            [
                                -95.504999999999995,
                                28.826000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348422-3638963",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348422-3638963",
                    "areaDesc": "Brazoria Islands",
                    "geocode": {
                        "UGC": [
                            "TXZ437"
                        ],
                        "SAME": [
                            "048039"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ437"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346519-3637772",
                            "identifier": "NWS-IDP-PROD-4346519-3637772",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T22:00:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345692-3637283",
                            "identifier": "NWS-IDP-PROD-4345692-3637283",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4345692-3637282",
                            "identifier": "NWS-IDP-PROD-4345692-3637282",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-23T16:16:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4346881-3638008",
                            "identifier": "NWS-IDP-PROD-4346881-3638008",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T03:40:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347175-3638177",
                            "identifier": "NWS-IDP-PROD-4347175-3638177",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:15:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347036-3638109",
                            "identifier": "NWS-IDP-PROD-4347036-3638109",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T07:26:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347708-3638482",
                            "identifier": "NWS-IDP-PROD-4347708-3638482",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T16:01:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T21:52:00-05:00",
                    "effective": "2020-07-24T21:52:00-05:00",
                    "onset": "2020-07-24T21:52:00-05:00",
                    "expires": "2020-07-25T06:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Observed",
                    "urgency": "Immediate",
                    "event": "Tropical Storm Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Tropical Storm Warning issued July 24 at 9:52PM CDT by NWS Houston/Galveston TX",
                    "description": "* WIND\n- LATEST LOCAL FORECAST: Below tropical storm force wind\n- Peak Wind Forecast: 20-30 mph with gusts to 35 mph\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Wind less than 39 mph\n- The wind threat has remained nearly steady from the\nprevious assessment.\n- PLAN: The sustained wind should remain less than tropical\nstorm force. Conditions may still be gusty.\n- PREPARE: Listen for any instructions from local officials.\n- ACT: Ensure emergency readiness should the forecast change.\n\n- REALIZED IMPACTS: Being Assessed\n- Little to no additional wind impacts expected. Community\nofficials are now assessing the extent of actual wind\nimpacts accordingly.\n\n* STORM SURGE\n- LATEST LOCAL FORECAST: Localized storm surge possible\n- Peak Storm Surge Inundation: The potential for 1-3 feet\nabove ground somewhere within surge prone areas\n- Window of concern: through Sunday afternoon\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for storm\nsurge flooding greater than 1 foot above ground\n- The storm surge threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Shelter against storm surge flooding greater than 1\nfoot above ground.\n- PREPARE: All flood preparations should be complete. Expect\nflooding of low-lying roads and property.\n- ACT: Stay away from storm surge prone areas. Continue to\nfollow the instructions of local officials.\n\n- POTENTIAL IMPACTS: Unfolding\n- Potential impacts from the main surge event are unfolding.\n\n* FLOODING RAIN\n- LATEST LOCAL FORECAST: Flash Flood Watch is in effect\n- Peak Rainfall Amounts: Additional 3-6 inches, with locally\nhigher amounts\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for\nmoderate flooding rain\n- The flooding rain threat has remained nearly steady from\nthe previous assessment.\n- PLAN: Emergency plans should include the potential for\nmoderate flooding from heavy rain. Evacuations and rescues\nare possible.\n- PREPARE: Consider protective actions if you are in an area\nvulnerable to flooding.\n- ACT: Heed any flood watches and warnings. Failure to take\naction may result in serious injury or loss of life.\n\n- POTENTIAL IMPACTS: Significant\n- Moderate rainfall flooding may prompt several evacuations\nand rescues.\n- Rivers and tributaries may quickly become swollen with\nswifter currents and overspill their banks in a few places,\nespecially in usually vulnerable spots. Small streams,\ncreeks, canals, and ditches overflow.\n- Flood waters can enter some structures or weaken\nfoundations. Several places may experience expanded areas\nof rapid inundation at underpasses, low-lying spots, and\npoor drainage areas. Some streets and parking lots take on\nmoving water as storm drains and retention ponds overflow.\nDriving conditions become hazardous. Some road and bridge\nclosures.\n\n* TORNADO\n- LATEST LOCAL FORECAST:\n- Situation is somewhat favorable for tornadoes\n\n- THREAT TO LIFE AND PROPERTY THAT INCLUDES TYPICAL FORECAST\nUNCERTAINTY IN TRACK, SIZE AND INTENSITY: Potential for a few\ntornadoes\n- The tornado threat has remained nearly steady from the\nprevious assessment.\n- PLAN: Plans should still include the potential for a few\ntornadoes.\n- PREPARE: Keep informed should additional weather alerts be\nneeded.\n- ACT: If a tornado warning is issued, be ready to shelter\nquickly.\n\n- POTENTIAL IMPACTS: Limited\n- The occurrence of isolated tornadoes can hinder the\nexecution of emergency plans during tropical events.\n- A few places may experience tornado damage, along with\npower and communications disruptions.\n- Locations could realize roofs peeled off buildings,\nchimneys toppled, mobile homes pushed off foundations or\noverturned, large tree tops and branches snapped off,\nshallow-rooted trees knocked over, moving vehicles blown\noff roads, and small boats pulled from moorings.",
                    "instruction": null,
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "TROPICAL STORM WARNING REMAINS IN EFFECT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.TR.W.1008.000000T0000Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXTCVHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348287-3638882",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -97.75,
                                28.370000000000001
                            ],
                            [
                                -97.650000000000006,
                                28.390000000000001
                            ],
                            [
                                -97.63000000000001,
                                28.330000000000002
                            ],
                            [
                                -97.480000000000004,
                                28.250000000000004
                            ],
                            [
                                -97.540000000000006,
                                28.170000000000005
                            ],
                            [
                                -97.690000000000012,
                                28.250000000000004
                            ],
                            [
                                -97.75,
                                28.370000000000001
                            ]
                        ]
                    ]
                },
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348287-3638882",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348287-3638882",
                    "areaDesc": "Bee, TX",
                    "geocode": {
                        "UGC": [
                            "TXC025"
                        ],
                        "SAME": [
                            "048025"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/county/TXC025"
                    ],
                    "references": [],
                    "sent": "2020-07-24T20:50:00-05:00",
                    "effective": "2020-07-24T20:50:00-05:00",
                    "onset": "2020-07-26T23:15:00-05:00",
                    "expires": "2020-07-25T12:00:00-05:00",
                    "ends": null,
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "event": "Flood Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Corpus Christi TX",
                    "headline": "Flood Warning issued July 24 at 8:50PM CDT by NWS Corpus Christi TX",
                    "description": "...The National Weather Service in Corpus Christi TX has issued a\nFlood Warning for the following river in Texas...\n\nAransas River near Skidmore affecting Bee County.\n\nFor the Aransas River...including Skidmore...Minor flooding is\nforecast.\n\nThe National Weather Service in Corpus Christi has issued a\n\n* Flood Warning for\nthe Aransas River Near Skidmore.\n* From Sunday evening until further notice.\n* At 8:15 PM CDT Friday the stage was 0.4 feet.\n* Flood stage is 13.0 feet.\n* Minor flooding is forecast.\n* Forecast...The river is expected to rise above flood stage Sunday\nevening, crest near 13.7 feet Sunday night, drop below flood stage\nearly Monday morning.\n* Impact...At 14.0 feet, moderate flooding occurs. Some roads are\nclosed. Crops and pasture land are threatened.",
                    "instruction": "Turn around, don't drown when encountering flooded roads. Most flood\ndeaths occur in vehicles.\n\nStay tuned to further developments by listening to your local radio,\ntelevision, or NOAA Weather Radio for further information.\n\nAdditional information is available at www.weather.gov/crp.",
                    "response": "Avoid",
                    "parameters": {
                        "VTEC": [
                            "/O.NEW.KCRP.FL.W.0008.200727T0415Z-000000T0000Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "CRPFLWCRP"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348008-3638709",
                "type": "Feature",
                "geometry": null,
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4348008-3638709",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4348008-3638709",
                    "areaDesc": "Coastal Cameron; Coastal Willacy; Coastal Kenedy",
                    "geocode": {
                        "UGC": [
                            "TXZ257",
                            "TXZ256",
                            "TXZ351"
                        ],
                        "SAME": [
                            "048061",
                            "048489",
                            "048261"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ257",
                        "https://api.weather.gov/zones/forecast/TXZ256",
                        "https://api.weather.gov/zones/forecast/TXZ351"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347239-3638239",
                            "identifier": "NWS-IDP-PROD-4347239-3638239",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T10:40:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T18:04:00-05:00",
                    "effective": "2020-07-24T18:04:00-05:00",
                    "onset": "2020-07-25T04:00:00-05:00",
                    "expires": "2020-07-25T03:00:00-05:00",
                    "ends": "2020-07-26T19:00:00-05:00",
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Minor",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "event": "Coastal Flood Advisory",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Brownsville TX",
                    "headline": "Coastal Flood Advisory issued July 24 at 6:04PM CDT until July 26 at 7:00PM CDT by NWS Brownsville TX",
                    "description": "* WHAT...Minor coastal flooding expected.\n\n* WHERE...Coastal Kenedy, Coastal Cameron and Coastal Willacy\nCounties.\n\n* WHEN...From 4 AM Saturday to 7 PM CDT Sunday.\n\n* IMPACTS...Nuisance flooding is expected, with water reaching\nor pushing into the dunes on South Padre Island. Vehicles,\nexcept those with four wheel drive and high wheel bases, will\nbe unable to be driven on the beach. This includes locations\nnorth of Public Beach Access #3. Minor to moderate beach\nerosion is expected.\n\n* ADDITIONAL DETAILS...These adverse beach conditions will be the\nresult of Tropical Storm Hanna making landfall along the South\nTexas Coast this weekend. Beach conditions are likely to be even\nmore adverse from the Port Mansfield jetty due to the close\nproximity of Hanna.",
                    "instruction": "If travel is required, allow extra time as some roads may be\nclosed. Do not drive around barricades or through water of\nunknown depth. Take the necessary actions to protect flood-prone\nproperty.",
                    "response": "Monitor",
                    "parameters": {
                        "NWSheadline": [
                            "COASTAL FLOOD ADVISORY REMAINS IN EFFECT FROM 4 AM SATURDAY TO 7 PM CDT SUNDAY"
                        ],
                        "VTEC": [
                            "/O.CON.KBRO.CF.Y.0006.200725T0900Z-200727T0000Z/"
                        ],
                        "PIL": [
                            "BROCFWBRO"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ],
                        "eventEndingTime": [
                            "2020-07-27T00:00:00+00:00"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347741-3638534",
                "type": "Feature",
                "geometry": null,
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347741-3638534",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4347741-3638534",
                    "areaDesc": "Matagorda Islands",
                    "geocode": {
                        "UGC": [
                            "TXZ436"
                        ],
                        "SAME": [
                            "048321"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ436"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347107-3638147",
                            "identifier": "NWS-IDP-PROD-4347107-3638147",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T09:23:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347107-3638146",
                            "identifier": "NWS-IDP-PROD-4347107-3638146",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T09:23:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T16:06:00-05:00",
                    "effective": "2020-07-24T16:06:00-05:00",
                    "onset": "2020-07-24T16:06:00-05:00",
                    "expires": "2020-07-25T00:15:00-05:00",
                    "ends": "2020-07-26T03:00:00-05:00",
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Moderate",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "event": "Rip Current Statement",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Rip Current Statement issued July 24 at 4:06PM CDT until July 26 at 3:00AM CDT by NWS Houston/Galveston TX",
                    "description": "* WHAT...For the Coastal Flood Advisory, minor coastal flooding.\nFor the High Rip Current Risk, dangerous rip currents.\n\n* WHERE...Matagorda Islands County.\n\n* WHEN...Through late Saturday night.\n\n* IMPACTS...Tides will reach 2-4 feet above normal between Port\nO'Connor and San Luis Pass, and 1-2 feet above normal between\nSan Luis Pass and High Island. Flooding of lots, parks, and\nroads with isolated road closures expected.\n\n* ADDITIONAL DETAILS...The Coastal Flood Advisory has been replaced\nwith a Storm Surge Warning.",
                    "instruction": "Swim near a lifeguard. If caught in a rip current, relax and\nfloat. Don't swim against the current. If able, swim in a\ndirection following the shoreline. If unable to escape, face the\nshore and call or wave for help.",
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "HIGH RIP CURRENT RISK REMAINS IN EFFECT THROUGH LATE SATURDAY NIGHT... ...COASTAL FLOOD ADVISORY IS CANCELLED"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.RP.S.0032.000000T0000Z-200726T0800Z/"
                        ],
                        "PIL": [
                            "HGXCFWHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ],
                        "eventEndingTime": [
                            "2020-07-26T08:00:00+00:00"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347743-3638539",
                "type": "Feature",
                "geometry": null,
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347743-3638539",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4347743-3638539",
                    "areaDesc": "Coastal Galveston; Coastal Harris",
                    "geocode": {
                        "UGC": [
                            "TXZ338",
                            "TXZ313"
                        ],
                        "SAME": [
                            "048167",
                            "048201"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ338",
                        "https://api.weather.gov/zones/forecast/TXZ313"
                    ],
                    "references": [],
                    "sent": "2020-07-24T16:06:00-05:00",
                    "effective": "2020-07-24T16:06:00-05:00",
                    "onset": "2020-07-24T16:06:00-05:00",
                    "expires": "2020-07-25T00:15:00-05:00",
                    "ends": "2020-07-26T03:00:00-05:00",
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "event": "Coastal Flood Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Coastal Flood Warning issued July 24 at 4:06PM CDT until July 26 at 3:00AM CDT by NWS Houston/Galveston TX",
                    "description": "* WHAT...Significant coastal flooding.\n\n* WHERE...Coastal Harris and Coastal Galveston Counties.\n\n* WHEN...Until 3 AM CDT Sunday.\n\n* IMPACTS...Numerous roads may be closed. Low lying property\nincluding homes, businesses, and some critical infrastructure\nwill be inundated. Some shoreline erosion will occur.",
                    "instruction": "Take the necessary actions to protect flood-prone property. If\ntravel is required, do not drive around barricades or through\nwater of unknown depth.",
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "COASTAL FLOOD WARNING IN EFFECT UNTIL 3 AM CDT SUNDAY"
                        ],
                        "VTEC": [
                            "/O.NEW.KHGX.CF.W.0001.200724T2106Z-200726T0800Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXCFWHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ],
                        "eventEndingTime": [
                            "2020-07-26T08:00:00+00:00"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347742-3638538",
                "type": "Feature",
                "geometry": null,
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347742-3638538",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4347742-3638538",
                    "areaDesc": "Brazoria Islands; Galveston Island and Bolivar Peninsula",
                    "geocode": {
                        "UGC": [
                            "TXZ437",
                            "TXZ438"
                        ],
                        "SAME": [
                            "048039",
                            "048167"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ437",
                        "https://api.weather.gov/zones/forecast/TXZ438"
                    ],
                    "references": [],
                    "sent": "2020-07-24T16:06:00-05:00",
                    "effective": "2020-07-24T16:06:00-05:00",
                    "onset": "2020-07-24T16:06:00-05:00",
                    "expires": "2020-07-25T00:15:00-05:00",
                    "ends": "2020-07-26T03:00:00-05:00",
                    "status": "Actual",
                    "messageType": "Alert",
                    "category": "Met",
                    "severity": "Severe",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "event": "Coastal Flood Warning",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Coastal Flood Warning issued July 24 at 4:06PM CDT until July 26 at 3:00AM CDT by NWS Houston/Galveston TX",
                    "description": "* WHAT...For the Coastal Flood Warning, significant coastal\nflooding. For the High Rip Current Risk, dangerous rip\ncurrents.\n\n* WHERE...Brazoria Islands and Galveston Island and Bolivar\nPeninsula Counties.\n\n* WHEN...For the Coastal Flood Warning, until 3 AM CDT Sunday.\nFor the High Rip Current Risk, through late Saturday night.\n\n* IMPACTS...Numerous roads may be closed. Low lying property\nincluding homes, businesses, and some critical infrastructure\nwill be inundated. Some shoreline erosion will occur. Rip\ncurrents can sweep even the best swimmers away from shore into\ndeeper water.",
                    "instruction": "Take the necessary actions to protect flood-prone property. If\ntravel is required, do not drive around barricades or through\nwater of unknown depth.\n\nSwim near a lifeguard. If caught in a rip current, relax and\nfloat. Don't swim against the current. If able, swim in a\ndirection following the shoreline. If unable to escape, face the\nshore and call or wave for help.",
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "COASTAL FLOOD WARNING IN EFFECT UNTIL 3 AM CDT SUNDAY... ...HIGH RIP CURRENT RISK REMAINS IN EFFECT THROUGH LATE SATURDAY NIGHT"
                        ],
                        "VTEC": [
                            "/O.NEW.KHGX.CF.W.0001.200724T2106Z-200726T0800Z/"
                        ],
                        "EAS-ORG": [
                            "WXR"
                        ],
                        "PIL": [
                            "HGXCFWHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ],
                        "eventEndingTime": [
                            "2020-07-26T08:00:00+00:00"
                        ]
                    }
                }
            },
            {
                "id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347742-3638537",
                "type": "Feature",
                "geometry": null,
                "properties": {
                    "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347742-3638537",
                    "@type": "wx:Alert",
                    "id": "NWS-IDP-PROD-4347742-3638537",
                    "areaDesc": "Brazoria Islands; Galveston Island and Bolivar Peninsula",
                    "geocode": {
                        "UGC": [
                            "TXZ437",
                            "TXZ438"
                        ],
                        "SAME": [
                            "048039",
                            "048167"
                        ]
                    },
                    "affectedZones": [
                        "https://api.weather.gov/zones/forecast/TXZ437",
                        "https://api.weather.gov/zones/forecast/TXZ438"
                    ],
                    "references": [
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347107-3638147",
                            "identifier": "NWS-IDP-PROD-4347107-3638147",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T09:23:00-05:00"
                        },
                        {
                            "@id": "https://api.weather.gov/alerts/NWS-IDP-PROD-4347107-3638146",
                            "identifier": "NWS-IDP-PROD-4347107-3638146",
                            "sender": "w-nws.webmaster@noaa.gov",
                            "sent": "2020-07-24T09:23:00-05:00"
                        }
                    ],
                    "sent": "2020-07-24T16:06:00-05:00",
                    "effective": "2020-07-24T16:06:00-05:00",
                    "onset": "2020-07-24T16:06:00-05:00",
                    "expires": "2020-07-25T00:15:00-05:00",
                    "ends": "2020-07-26T03:00:00-05:00",
                    "status": "Actual",
                    "messageType": "Update",
                    "category": "Met",
                    "severity": "Moderate",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "event": "Rip Current Statement",
                    "sender": "w-nws.webmaster@noaa.gov",
                    "senderName": "NWS Houston/Galveston TX",
                    "headline": "Rip Current Statement issued July 24 at 4:06PM CDT until July 26 at 3:00AM CDT by NWS Houston/Galveston TX",
                    "description": "* WHAT...For the Coastal Flood Warning, significant coastal\nflooding. For the High Rip Current Risk, dangerous rip\ncurrents.\n\n* WHERE...Brazoria Islands and Galveston Island and Bolivar\nPeninsula Counties.\n\n* WHEN...For the Coastal Flood Warning, until 3 AM CDT Sunday.\nFor the High Rip Current Risk, through late Saturday night.\n\n* IMPACTS...Numerous roads may be closed. Low lying property\nincluding homes, businesses, and some critical infrastructure\nwill be inundated. Some shoreline erosion will occur. Rip\ncurrents can sweep even the best swimmers away from shore into\ndeeper water.",
                    "instruction": "Take the necessary actions to protect flood-prone property. If\ntravel is required, do not drive around barricades or through\nwater of unknown depth.\n\nSwim near a lifeguard. If caught in a rip current, relax and\nfloat. Don't swim against the current. If able, swim in a\ndirection following the shoreline. If unable to escape, face the\nshore and call or wave for help.",
                    "response": "Avoid",
                    "parameters": {
                        "NWSheadline": [
                            "COASTAL FLOOD WARNING IN EFFECT UNTIL 3 AM CDT SUNDAY... ...HIGH RIP CURRENT RISK REMAINS IN EFFECT THROUGH LATE SATURDAY NIGHT"
                        ],
                        "VTEC": [
                            "/O.CON.KHGX.RP.S.0032.000000T0000Z-200726T0800Z/"
                        ],
                        "PIL": [
                            "HGXCFWHGX"
                        ],
                        "BLOCKCHANNEL": [
                            "CMAS",
                            "EAS",
                            "NWEM"
                        ],
                        "eventEndingTime": [
                            "2020-07-26T08:00:00+00:00"
                        ]
                    }
                }
            }
        ],
        "title": "current watches, warnings, and advisories for Texas",
        "updated": "2020-07-25T06:00:00+00:00"
    }
    -------------------FORECASTS GRID--------------------------------
    https://api.weather.gov/points/39.7456,-97.0892
    {
        "@context": [
            "https://geojson.org/geojson-ld/geojson-context.jsonld",
            {
                "@version": "1.1",
                "wx": "https://api.weather.gov/ontology#",
                "s": "https://schema.org/",
                "geo": "http://www.opengis.net/ont/geosparql#",
                "unit": "http://codes.wmo.int/common/unit/",
                "@vocab": "https://api.weather.gov/ontology#",
                "geometry": {
                    "@id": "s:GeoCoordinates",
                    "@type": "geo:wktLiteral"
                },
                "city": "s:addressLocality",
                "state": "s:addressRegion",
                "distance": {
                    "@id": "s:Distance",
                    "@type": "s:QuantitativeValue"
                },
                "bearing": {
                    "@type": "s:QuantitativeValue"
                },
                "value": {
                    "@id": "s:value"
                },
                "unitCode": {
                    "@id": "s:unitCode",
                    "@type": "@id"
                },
                "forecastOffice": {
                    "@type": "@id"
                },
                "forecastGridData": {
                    "@type": "@id"
                },
                "publicZone": {
                    "@type": "@id"
                },
                "county": {
                    "@type": "@id"
                }
            }
        ],
        "id": "https://api.weather.gov/points/39.7456,-97.0892",
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                -97.089200000000005,
                39.745600000000003
            ]
        },
        "properties": {
            "@id": "https://api.weather.gov/points/39.7456,-97.0892",
            "@type": "wx:Point",
            "cwa": "TOP",
            "forecastOffice": "https://api.weather.gov/offices/TOP",
            "gridId": "TOP",
            "gridX": 31,
            "gridY": 80,
            "forecast": "https://api.weather.gov/gridpoints/TOP/31,80/forecast",
            "forecastHourly": "https://api.weather.gov/gridpoints/TOP/31,80/forecast/hourly",
            "forecastGridData": "https://api.weather.gov/gridpoints/TOP/31,80",
            "observationStations": "https://api.weather.gov/gridpoints/TOP/31,80/stations",
            "relativeLocation": {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -97.086661000000007,
                        39.679375999999998
                    ]
                },
                "properties": {
                    "city": "Linn",
                    "state": "KS",
                    "distance": {
                        "value": 7366.9851976443997,
                        "unitCode": "unit:m"
                    },
                    "bearing": {
                        "value": 358,
                        "unitCode": "unit:degrees_true"
                    }
                }
            },
            "forecastZone": "https://api.weather.gov/zones/forecast/KSZ009",
            "county": "https://api.weather.gov/zones/county/KSC201",
            "fireWeatherZone": "https://api.weather.gov/zones/fire/KSZ009",
            "timeZone": "America/Chicago",
            "radarStation": "KTWX"
        }
    }
    {
        "@context": [
            "https://geojson.org/geojson-ld/geojson-context.jsonld",
            {
                "@version": "1.1",
                "wx": "https://api.weather.gov/ontology#",
                "s": "https://schema.org/",
                "geo": "http://www.opengis.net/ont/geosparql#",
                "unit": "http://codes.wmo.int/common/unit/",
                "@vocab": "https://api.weather.gov/ontology#",
                "geometry": {
                    "@id": "s:GeoCoordinates",
                    "@type": "geo:wktLiteral"
                },
                "city": "s:addressLocality",
                "state": "s:addressRegion",
                "distance": {
                    "@id": "s:Distance",
                    "@type": "s:QuantitativeValue"
                },
                "bearing": {
                    "@type": "s:QuantitativeValue"
                },
                "value": {
                    "@id": "s:value"
                },
                "unitCode": {
                    "@id": "s:unitCode",
                    "@type": "@id"
                },
                "forecastOffice": {
                    "@type": "@id"
                },
                "forecastGridData": {
                    "@type": "@id"
                },
                "publicZone": {
                    "@type": "@id"
                },
                "county": {
                    "@type": "@id"
                }
            }
        ],
        "id": "https://api.weather.gov/points/39.7456,-97.0892",
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                -97.089200000000005,
                39.745600000000003
            ]
        },
        "properties": {
            "@id": "https://api.weather.gov/points/39.7456,-97.0892",
            "@type": "wx:Point",
            "cwa": "TOP",
            "forecastOffice": "https://api.weather.gov/offices/TOP",
            "gridId": "TOP",
            "gridX": 31,
            "gridY": 80,
            "forecast": "https://api.weather.gov/gridpoints/TOP/31,80/forecast",
            "forecastHourly": "https://api.weather.gov/gridpoints/TOP/31,80/forecast/hourly",
            "forecastGridData": "https://api.weather.gov/gridpoints/TOP/31,80",
            "observationStations": "https://api.weather.gov/gridpoints/TOP/31,80/stations",
            "relativeLocation": {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -97.086661000000007,
                        39.679375999999998
                    ]
                },
                "properties": {
                    "city": "Linn",
                    "state": "KS",
                    "distance": {
                        "value": 7366.9851976443997,
                        "unitCode": "unit:m"
                    },
                    "bearing": {
                        "value": 358,
                        "unitCode": "unit:degrees_true"
                    }
                }
            },
            "forecastZone": "https://api.weather.gov/zones/forecast/KSZ009",
            "county": "https://api.weather.gov/zones/county/KSC201",
            "fireWeatherZone": "https://api.weather.gov/zones/fire/KSZ009",
            "timeZone": "America/Chicago",
            "radarStation": "KTWX"
        }
    }
    -------------------FORECASTS--------------------------------
    https://api.weather.gov/gridpoints/TOP/31,80/forecast
    {'@context': ['https://geojson.org/geojson-ld/geojson-context.jsonld', {'@version': '1.1', 'wx': 'https://api.weather.gov/ontology#', 'geo': 'http://www.opengis.net/ont/geosparql#', 'unit': 'http://codes.wmo.int/common/unit/', '@vocab': 'https://api.weather.gov/ontology#'}], 'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[-97.1089731, 39.7668263], [-97.1085269, 39.7447788], [-97.0798467, 39.7451195], [-97.08028680000001, 39.767167], [-97.1089731, 39.7668263]]]}, 'properties': {'updated': '2020-07-25T08:10:03+00:00', 'units': 'us', 'forecastGenerator': 'BaselineForecastGenerator', 'generatedAt': '2020-07-25T08:25:53+00:00', 'updateTime': '2020-07-25T08:10:03+00:00', 'validTimes': '2020-07-25T02:00:00+00:00/P6DT23H', 'elevation': {'value': 441.96, 'unitCode': 'unit:m'}, 'periods': [{'number': 1, 'name': 'Overnight', 'startTime': '2020-07-25T03:00:00-05:00', 'endTime': '2020-07-25T06:00:00-05:00', 'isDaytime': False, 'temperature': 74, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '10 mph', 'windDirection': 'S', 'icon': 'https://api.weather.gov/icons/land/night/few?size=medium', 'shortForecast': 'Mostly Clear', 'detailedForecast': 'Mostly clear, with a low around 74. South wind around 10 mph.'}, {'number': 2, 'name': 'Saturday', 'startTime': '2020-07-25T06:00:00-05:00', 'endTime': '2020-07-25T18:00:00-05:00', 'isDaytime': True, 'temperature': 93, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '10 to 15 mph', 'windDirection': 'S', 'icon': 'https://api.weather.gov/icons/land/day/sct?size=medium', 'shortForecast': 'Mostly Sunny', 'detailedForecast': 'Mostly sunny, with a high near 93. South wind 10 to 15 mph, with gusts as high as 25 mph.'}, {'number': 3, 'name': 'Saturday Night', 'startTime': '2020-07-25T18:00:00-05:00', 'endTime': '2020-07-26T06:00:00-05:00', 'isDaytime': False, 'temperature': 75, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '10 to 15 mph', 'windDirection': 'S', 'icon': 'https://api.weather.gov/icons/land/night/few?size=medium', 'shortForecast': 'Mostly Clear', 'detailedForecast': 'Mostly clear, with a low around 75. South wind 10 to 15 mph, with gusts as high as 20 mph.'}, {'number': 4, 'name': 'Sunday', 'startTime': '2020-07-26T06:00:00-05:00', 'endTime': '2020-07-26T18:00:00-05:00', 'isDaytime': True, 'temperature': 91, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '5 to 10 mph', 'windDirection': 'S', 'icon': 'https://api.weather.gov/icons/land/day/tsra_hi,20/tsra_hi,50?size=medium', 'shortForecast': 'Chance Showers And Thunderstorms', 'detailedForecast': 'A chance of showers and thunderstorms after 7am. Mostly sunny, with a high near 91. South wind 5 to 10 mph. Chance of precipitation is 50%.'}, {'number': 5, 'name': 'Sunday Night', 'startTime': '2020-07-26T18:00:00-05:00', 'endTime': '2020-07-27T06:00:00-05:00', 'isDaytime': False, 'temperature': 69, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '0 to 5 mph', 'windDirection': 'NE', 'icon': 'https://api.weather.gov/icons/land/night/tsra_sct,70/tsra_sct,90?size=medium', 'shortForecast': 'Showers And Thunderstorms', 'detailedForecast': 'Showers and thunderstorms. Mostly cloudy, with a low around 69. Northeast wind 0 to 5 mph. Chance of precipitation is 90%.'}, {'number': 6, 'name': 'Monday', 'startTime': '2020-07-27T06:00:00-05:00', 'endTime': '2020-07-27T18:00:00-05:00', 'isDaytime': True, 'temperature': 80, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '5 to 10 mph', 'windDirection': 'NE', 'icon': 'https://api.weather.gov/icons/land/day/tsra_hi,90/tsra_hi,50?size=medium', 'shortForecast': 'Showers And Thunderstorms', 'detailedForecast': 'Showers and thunderstorms. Partly sunny, with a high near 80. Northeast wind 5 to 10 mph. Chance of precipitation is 90%.'}, {'number': 7, 'name': 'Monday Night', 'startTime': '2020-07-27T18:00:00-05:00', 'endTime': '2020-07-28T06:00:00-05:00', 'isDaytime': False, 'temperature': 61, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '0 to 5 mph', 'windDirection': 'NE', 'icon': 'https://api.weather.gov/icons/land/night/tsra_hi,20/sct?size=medium', 'shortForecast': 'Slight Chance Showers And Thunderstorms then Partly Cloudy', 'detailedForecast': 'A slight chance of showers and thunderstorms before 7pm. Partly cloudy, with a low around 61. Northeast wind 0 to 5 mph. Chance of precipitation is 20%.'}, {'number': 8, 'name': 'Tuesday', 'startTime': '2020-07-28T06:00:00-05:00', 'endTime': '2020-07-28T18:00:00-05:00', 'isDaytime': True, 'temperature': 82, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '0 to 5 mph', 'windDirection': 'SE', 'icon': 'https://api.weather.gov/icons/land/day/few?size=medium', 'shortForecast': 'Sunny', 'detailedForecast': 'Sunny, with a high near 82. Southeast wind 0 to 5 mph.'}, {'number': 9, 'name': 'Tuesday Night', 'startTime': '2020-07-28T18:00:00-05:00', 'endTime': '2020-07-29T06:00:00-05:00', 'isDaytime': False, 'temperature': 64, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '0 to 5 mph', 'windDirection': 'SE', 'icon': 'https://api.weather.gov/icons/land/night/bkn/tsra_hi,20?size=medium', 'shortForecast': 'Mostly Cloudy then Slight Chance Showers And Thunderstorms', 'detailedForecast': 'A slight chance of showers and thunderstorms after 1am. Mostly cloudy, with a low around 64. Southeast wind 0 to 5 mph. Chance of precipitation is 20%.'}, {'number': 10, 'name': 'Wednesday', 'startTime': '2020-07-29T06:00:00-05:00', 'endTime': '2020-07-29T18:00:00-05:00', 'isDaytime': True, 'temperature': 81, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '5 mph', 'windDirection': 'S', 'icon': 'https://api.weather.gov/icons/land/day/tsra_hi,20/tsra_hi,30?size=medium', 'shortForecast': 'Chance Showers And Thunderstorms', 'detailedForecast': 'A chance of showers and thunderstorms. Partly sunny, with a high near 81. Chance of precipitation is 30%.'}, {'number': 11, 'name': 'Wednesday Night', 'startTime': '2020-07-29T18:00:00-05:00', 'endTime': '2020-07-30T06:00:00-05:00', 'isDaytime': False, 'temperature': 66, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '5 mph', 'windDirection': 'SE', 'icon': 'https://api.weather.gov/icons/land/night/tsra_hi,30?size=medium', 'shortForecast': 'Chance Showers And Thunderstorms', 'detailedForecast': 'A chance of showers and thunderstorms. Partly cloudy, with a low around 66. Chance of precipitation is 30%.'}, {'number': 12, 'name': 'Thursday', 'startTime': '2020-07-30T06:00:00-05:00', 'endTime': '2020-07-30T18:00:00-05:00', 'isDaytime': True, 'temperature': 84, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '5 mph', 'windDirection': 'S', 'icon': 'https://api.weather.gov/icons/land/day/tsra_hi,30?size=medium', 'shortForecast': 'Chance Showers And Thunderstorms', 'detailedForecast': 'A chance of showers and thunderstorms. Sunny, with a high near 84. Chance of precipitation is 30%.'}, {'number': 13, 'name': 'Thursday Night', 'startTime': '2020-07-30T18:00:00-05:00', 'endTime': '2020-07-31T06:00:00-05:00', 'isDaytime': False, 'temperature': 66, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '0 to 5 mph', 'windDirection': 'SE', 'icon': 'https://api.weather.gov/icons/land/night/tsra_hi,30?size=medium', 'shortForecast': 'Chance Showers And Thunderstorms', 'detailedForecast': 'A chance of showers and thunderstorms. Partly cloudy, with a low around 66. Chance of precipitation is 30%.'}, {'number': 14, 'name': 'Friday', 'startTime': '2020-07-31T06:00:00-05:00', 'endTime': '2020-07-31T18:00:00-05:00', 'isDaytime': True, 'temperature': 81, 'temperatureUnit': 'F', 'temperatureTrend': None, 'windSpeed': '0 to 5 mph', 'windDirection': 'SE', 'icon': 'https://api.weather.gov/icons/land/day/tsra_hi,30/tsra_hi,20?size=medium', 'shortForecast': 'Chance Showers And Thunderstorms', 'detailedForecast': 'A chance of showers and thunderstorms. Mostly sunny, with a high near 81. Chance of precipitation is 30%.'}]}}

    {
    @context: [
    "https://geojson.org/geojson-ld/geojson-context.jsonld",
    {
    @version: "1.1",
    wx: "https://api.weather.gov/ontology#",
    geo: "http://www.opengis.net/ont/geosparql#",
    unit: "http://codes.wmo.int/common/unit/",
    @vocab: "https://api.weather.gov/ontology#"
    }
    ],
    type: "Feature",
    geometry: {
    type: "Polygon",
    coordinates: [
    [
    [
    -97.1089731,
    39.7668263
    ],
    [
    -97.1085269,
    39.7447788
    ],
    [
    -97.0798467,
    39.7451195
    ],
    [
    -97.08028680000001,
    39.767167
    ],
    [
    -97.1089731,
    39.7668263
    ]
    ]
    ]
    },
    properties: {
    updated: "2020-07-25T08:10:03+00:00",
    units: "us",
    forecastGenerator: "BaselineForecastGenerator",
    generatedAt: "2020-07-25T08:31:44+00:00",
    updateTime: "2020-07-25T08:10:03+00:00",
    validTimes: "2020-07-25T02:00:00+00:00/P6DT23H",
    elevation: {
    value: 441.96,
    unitCode: "unit:m"
    },
    periods: [
    {
    number: 1,
    name: "Overnight",
    startTime: "2020-07-25T03:00:00-05:00",
    endTime: "2020-07-25T06:00:00-05:00",
    isDaytime: false,
    temperature: 74,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "10 mph",
    windDirection: "S",
    icon: "https://api.weather.gov/icons/land/night/few?size=medium",
    shortForecast: "Mostly Clear",
    detailedForecast: "Mostly clear, with a low around 74. South wind around 10 mph."
    },
    {
    number: 2,
    name: "Saturday",
    startTime: "2020-07-25T06:00:00-05:00",
    endTime: "2020-07-25T18:00:00-05:00",
    isDaytime: true,
    temperature: 93,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "10 to 15 mph",
    windDirection: "S",
    icon: "https://api.weather.gov/icons/land/day/sct?size=medium",
    shortForecast: "Mostly Sunny",
    detailedForecast: "Mostly sunny, with a high near 93. South wind 10 to 15 mph, with gusts as high as 25 mph."
    },
    {
    number: 3,
    name: "Saturday Night",
    startTime: "2020-07-25T18:00:00-05:00",
    endTime: "2020-07-26T06:00:00-05:00",
    isDaytime: false,
    temperature: 75,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "10 to 15 mph",
    windDirection: "S",
    icon: "https://api.weather.gov/icons/land/night/few?size=medium",
    shortForecast: "Mostly Clear",
    detailedForecast: "Mostly clear, with a low around 75. South wind 10 to 15 mph, with gusts as high as 20 mph."
    },
    {
    number: 4,
    name: "Sunday",
    startTime: "2020-07-26T06:00:00-05:00",
    endTime: "2020-07-26T18:00:00-05:00",
    isDaytime: true,
    temperature: 91,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "5 to 10 mph",
    windDirection: "S",
    icon: "https://api.weather.gov/icons/land/day/tsra_hi,20/tsra_hi,50?size=medium",
    shortForecast: "Chance Showers And Thunderstorms",
    detailedForecast: "A chance of showers and thunderstorms after 7am. Mostly sunny, with a high near 91. South wind 5 to 10 mph. Chance of precipitation is 50%."
    },
    {
    number: 5,
    name: "Sunday Night",
    startTime: "2020-07-26T18:00:00-05:00",
    endTime: "2020-07-27T06:00:00-05:00",
    isDaytime: false,
    temperature: 69,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "0 to 5 mph",
    windDirection: "NE",
    icon: "https://api.weather.gov/icons/land/night/tsra_sct,70/tsra_sct,90?size=medium",
    shortForecast: "Showers And Thunderstorms",
    detailedForecast: "Showers and thunderstorms. Mostly cloudy, with a low around 69. Northeast wind 0 to 5 mph. Chance of precipitation is 90%."
    },
    {
    number: 6,
    name: "Monday",
    startTime: "2020-07-27T06:00:00-05:00",
    endTime: "2020-07-27T18:00:00-05:00",
    isDaytime: true,
    temperature: 80,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "5 to 10 mph",
    windDirection: "NE",
    icon: "https://api.weather.gov/icons/land/day/tsra_hi,90/tsra_hi,50?size=medium",
    shortForecast: "Showers And Thunderstorms",
    detailedForecast: "Showers and thunderstorms. Partly sunny, with a high near 80. Northeast wind 5 to 10 mph. Chance of precipitation is 90%."
    },
    {
    number: 7,
    name: "Monday Night",
    startTime: "2020-07-27T18:00:00-05:00",
    endTime: "2020-07-28T06:00:00-05:00",
    isDaytime: false,
    temperature: 61,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "0 to 5 mph",
    windDirection: "NE",
    icon: "https://api.weather.gov/icons/land/night/tsra_hi,20/sct?size=medium",
    shortForecast: "Slight Chance Showers And Thunderstorms then Partly Cloudy",
    detailedForecast: "A slight chance of showers and thunderstorms before 7pm. Partly cloudy, with a low around 61. Northeast wind 0 to 5 mph. Chance of precipitation is 20%."
    },
    {
    number: 8,
    name: "Tuesday",
    startTime: "2020-07-28T06:00:00-05:00",
    endTime: "2020-07-28T18:00:00-05:00",
    isDaytime: true,
    temperature: 82,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "0 to 5 mph",
    windDirection: "SE",
    icon: "https://api.weather.gov/icons/land/day/few?size=medium",
    shortForecast: "Sunny",
    detailedForecast: "Sunny, with a high near 82. Southeast wind 0 to 5 mph."
    },
    {
    number: 9,
    name: "Tuesday Night",
    startTime: "2020-07-28T18:00:00-05:00",
    endTime: "2020-07-29T06:00:00-05:00",
    isDaytime: false,
    temperature: 64,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "0 to 5 mph",
    windDirection: "SE",
    icon: "https://api.weather.gov/icons/land/night/bkn/tsra_hi,20?size=medium",
    shortForecast: "Mostly Cloudy then Slight Chance Showers And Thunderstorms",
    detailedForecast: "A slight chance of showers and thunderstorms after 1am. Mostly cloudy, with a low around 64. Southeast wind 0 to 5 mph. Chance of precipitation is 20%."
    },
    {
    number: 10,
    name: "Wednesday",
    startTime: "2020-07-29T06:00:00-05:00",
    endTime: "2020-07-29T18:00:00-05:00",
    isDaytime: true,
    temperature: 81,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "5 mph",
    windDirection: "S",
    icon: "https://api.weather.gov/icons/land/day/tsra_hi,20/tsra_hi,30?size=medium",
    shortForecast: "Chance Showers And Thunderstorms",
    detailedForecast: "A chance of showers and thunderstorms. Partly sunny, with a high near 81. Chance of precipitation is 30%."
    },
    {
    number: 11,
    name: "Wednesday Night",
    startTime: "2020-07-29T18:00:00-05:00",
    endTime: "2020-07-30T06:00:00-05:00",
    isDaytime: false,
    temperature: 66,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "5 mph",
    windDirection: "SE",
    icon: "https://api.weather.gov/icons/land/night/tsra_hi,30?size=medium",
    shortForecast: "Chance Showers And Thunderstorms",
    detailedForecast: "A chance of showers and thunderstorms. Partly cloudy, with a low around 66. Chance of precipitation is 30%."
    },
    {
    number: 12,
    name: "Thursday",
    startTime: "2020-07-30T06:00:00-05:00",
    endTime: "2020-07-30T18:00:00-05:00",
    isDaytime: true,
    temperature: 84,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "5 mph",
    windDirection: "S",
    icon: "https://api.weather.gov/icons/land/day/tsra_hi,30?size=medium",
    shortForecast: "Chance Showers And Thunderstorms",
    detailedForecast: "A chance of showers and thunderstorms. Sunny, with a high near 84. Chance of precipitation is 30%."
    },
    {
    number: 13,
    name: "Thursday Night",
    startTime: "2020-07-30T18:00:00-05:00",
    endTime: "2020-07-31T06:00:00-05:00",
    isDaytime: false,
    temperature: 66,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "0 to 5 mph",
    windDirection: "SE",
    icon: "https://api.weather.gov/icons/land/night/tsra_hi,30?size=medium",
    shortForecast: "Chance Showers And Thunderstorms",
    detailedForecast: "A chance of showers and thunderstorms. Partly cloudy, with a low around 66. Chance of precipitation is 30%."
    },
    {
    number: 14,
    name: "Friday",
    startTime: "2020-07-31T06:00:00-05:00",
    endTime: "2020-07-31T18:00:00-05:00",
    isDaytime: true,
    temperature: 81,
    temperatureUnit: "F",
    temperatureTrend: null,
    windSpeed: "0 to 5 mph",
    windDirection: "SE",
    icon: "https://api.weather.gov/icons/land/day/tsra_hi,30/tsra_hi,20?size=medium",
    shortForecast: "Chance Showers And Thunderstorms",
    detailedForecast: "A chance of showers and thunderstorms. Mostly sunny, with a high near 81. Chance of precipitation is 30%."
    }
    ]
    }
    }

    D:\www\noaa_weather>

    """

