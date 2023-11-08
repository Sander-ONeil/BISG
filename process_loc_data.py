import numpy as np
locdata = np.loadtxt('census_loc_data.csv',
                 delimiter=",", dtype=str)
                 
empty = np.loadtxt('census_loc_data.csv',
                 delimiter=",", dtype=str)
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

locdata[:,2] = PCT2PRACE.astype(str)
locdata[:,3] = PCTAIAN.astype(str)
locdata[:,4] = PCTAPI.astype(str)
locdata[:,5] = PCTBLACK.astype(str)
locdata[:,6] = PCTHISPANIC.astype(str)
locdata[:,7] = PCTWHITE.astype(str)

empty[1:] = locdata

empty = empty.astype(str)

import pandas as pd
import numpy as np
 

# convert array into dataframe
DF = pd.DataFrame(empty)
 
# save the dataframe as a csv file
DF.to_csv("census_loc_data_same_format.csv")