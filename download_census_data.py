import requests


N = 100000
# The URL of the Census API for the 2010 surname data
url = "https://api.census.gov/data/2010/surname?get=NAME,COUNT,PCT2PRACE,PCTAIAN,PCTAPI,PCTBLACK,PCTHISPANIC,PCTWHITE&RANK=1:" + str(N)

# Make a GET request to the API
response = requests.get(url)

js = response.json()
print(js[0])


import csv
with open('census_data_rank_1:'+str(N)+'.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Writing the data into the file
    writer.writerows(js)

