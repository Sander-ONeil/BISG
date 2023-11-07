import requests




datapoints = {
    "DP1_0085C": "T",
    "DP1_0086C": "White",
    "DP1_0087C": "Black",
    "DP1_0088C": "American Indian and Alaska Native",
    "DP1_0089C": "Asian",
    "DP1_0090C": "Native Hawaiian and Other Pacific Islander",
    "DP1_0091C": "Some Other Race"
}
# matching with other dataset
datapoints = {
    "NAME": "Name",  # Assuming you meant to have "Name" as both key and value. If not, adjust accordingly.
    "DP1_0076C": "Count!!RACE!!Total population",
    "DP1_0084P": "Two or More Races",
    "DP1_0080P": "One Race!!American Indian and Alaska Native",
    "DP1_0082P": "One Race!!Native Hawaiian and Other Pacific Islander",
    "DP1_0079P": "One Race!!Black or African American",
    #"DP1_0092P": "Percent!!HISPANIC OR LATINO!!Total population",
    "DP1_0093P": "Hispanic or Latino (of any race)",
    "DP1_0078P": "One Race!!White",
}

for d in datapoints.keys():
    
    print(d,end=',')

names = list(datapoints.values())
names =  names + ['Zip Code Area']


url = "https://api.census.gov/data/2020/dec/dp?get=NAME,DP1_0076C,DP1_0084P,DP1_0080P,DP1_0082P,DP1_0079P,DP1_0093P,DP1_0078P&for=zip%20code%20tabulation%20area:*"

# Make a GET request to the API
response = requests.get(url)


js = response.json()
print(js[0])


import csv
with open('census_loc_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Writing the data into the file
    writer.writerow(names)
    writer.writerows(js[1:len(js)])
    
