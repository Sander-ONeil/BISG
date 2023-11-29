import random_address
import numpy as np
td = np.loadtxt('testdata.csv',delimiter=",", dtype=str)
import pgeocode

nomi = pgeocode.Nominatim('us')

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercises")


for z in td[:,1]:
    r = nomi.query_postal_code(z)
    print(z)
    lat = r['latitude']
    lon = r['longitude']
    
    lls = str(lat)+","+str(lon)
    # print(lls)
    
    
    # location = geolocator.reverse(lls)
 
    # # Display
    # print(location)
    
    print(lat,lon)
