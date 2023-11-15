import requests


N = 100000
# The URL of the Census API for the 2010 surname data
url = "https://api.census.gov/data/2010/surname?get=NAME,COUNT,PCT2PRACE,PCTAIAN,PCTAPI,PCTBLACK,PCTHISPANIC,PCTWHITE&RANK=1:" + str(N)
print(url)
# Make a GET request to the API
response = requests.get(url)

js = response.json()
print(js[0])
nameheader = js[0]
filename = ('census_name_data_rank_1_'+str(N)+'.csv')
print(filename)


import csv
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Writing the data into the file
    writer.writerows(js)


url = "https://api.census.gov/data/2020/dec/dp?get=NAME,DP1_0076C,DP1_0111C,DP1_0107C,DP1_0109C,DP1_0106C,DP1_0108C,DP1_0096C,DP1_0105C&for=zip%20code%20tabulation%20area:*"

# Make a GET request to the API
response = requests.get(url)


js = response.json()
print(js[0])

import numpy as np
L = np.array(js)

datapoints = {
    "NAME":"name",
"DP1_0076C": "Count!!RACE!!Total population",
'DP1_0111C':	'Not Hispanic or Latino!!Two or More Races',
'DP1_0107C':	'Not Hispanic or Latino!!American Indian and Alaska Native alone',
'DP1_0109C':	'Not Hispanic or Latino!!Native Hawaiian and Other Pacific Islander alone',
'DP1_0106C':	'Not Hispanic or Latino!!Black or African American alone',
'DP1_0108C':	'Not Hispanic or Latino!!Asian alone',
'DP1_0096C':	'Hispanic or Latino',
'DP1_0105C':	'Not Hispanic or Latino!!White alone',
}
for d in datapoints.keys():
    
    print(d,end=',')

names = list(datapoints.values())
names =  names + ['Zip Code Area']

import csv
with open('census_loc_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Writing the data into the file
    writer.writerow(names)
    writer.writerows(js[1:len(js)])
    

import numpy as np
locdata = np.loadtxt('census_loc_data.csv',
                 delimiter=",", dtype=str)
                 
empty = np.zeros((locdata.shape[0],9),dtype = 'U25')
print(locdata.shape)
lheader = locdata[0,:]
print(lheader)
locdata = locdata[1:locdata.shape[0]]

D = locdata[:,1:].astype(float)



D[:,1:] /= D[:,0][:,np.newaxis]
D[:,1:]*=100

PCT2PRACE,PCTAIAN,PCTAPI,PCTBLACK,PCTHISPANIC,PCTWHITE = (D[:,1],D[:,2],D[:,3]+D[:,5],D[:,4],D[:,6],D[:,7])

print('\nPCT2PRACE',PCT2PRACE,'\nPCTAIAN',PCTAIAN,'\nPCTAPI',PCTAPI,'\nPCTBLACK',PCTBLACK,'\nPCTHISPANIC',PCTHISPANIC,'\nPCTWHITE',PCTWHITE)

Races = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7}

empty[1:,0] = locdata[:,0] 
empty[1:,1] = locdata[:,1]
empty[1:,2] = PCT2PRACE.astype(str)
empty[1:,3] = PCTAIAN.astype(str)
empty[1:,4] = PCTAPI.astype(str)
empty[1:,5] = PCTBLACK.astype(str)
empty[1:,6] = PCTHISPANIC.astype(str)
empty[1:,7] = PCTWHITE.astype(str)
empty[1:,8] = locdata[:,9]
empty[0] = ['NAME','COUNT','PCT2PRACE','PCTAIAN','PCTAPI','PCTBLACK','PCTHISPANIC','PCTWHITE','zipcode']


empty = empty.astype(str)

import pandas as pd
import numpy as np
 

# convert array into dataframe
DF = pd.DataFrame(empty)
 
# save the dataframe as a csv file
DF.to_csv("census_loc_data_same_format.csv")