import numpy as np

# data of person to examine
fname = 'penelope'
fname = fname.upper()
surname = 'smith'
surname = surname.upper()

zipcode = '10475'


#loading data from csv into numpy
def load_data(file_name):
    data = np.loadtxt(file_name, delimiter=",", dtype=str)
    return data

namedata = load_data('census_name_data_rank_1_100000.csv')
nheader = namedata[0,:]
namedata = namedata[1:namedata.shape[0]]
namedata[namedata =='(S)'] = '0'

# this data is wierdly formatted so it takes of first column and row; could solve but would have to change multiple files in github
locdata = load_data('census_loc_data_same_format.csv')[1:,1:]
lheader = locdata[0,:]
locdata = locdata[1:locdata.shape[0]]


fnamedata = load_data('fnamedata.csv')
fheader = fnamedata[0,:]
fnamedata = fnamedata[1:fnamedata.shape[0]]
total_fname_count = np.sum(fnamedata[:,1].astype(float))
print(fnamedata.shape)
print(total_fname_count) #name count lower than total pop significantly. Should use this to get prob I think, depends if its representative sample, if every instance of these names are counted then could divide by us pop

# total data for US
Totals = np.array([["NAME","DP1_0076C","DP1_0084P","DP1_0080P","DP1_0082P","DP1_0079P","DP1_0093P","DP1_0078P","us"],
["United States","331449281","4.08779979","0.67934949","6.10673734","12.05021108","18.72987741","57.83619335","1"]])


def sortbycount(data,i = 1):
    ind = np.argsort(-data[:,i].astype(float), axis=0)
    return data[ind]

n = 10

F = sortbycount(fnamedata)[:n,0]
L = sortbycount(locdata)[:n,8]
N = sortbycount(namedata)[:n,0]

print(F[:3],N[:3],L[:3])

races = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7}

for x in races:
    i = races[x]
    F1 = sortbycount(fnamedata,i)
    L1 = sortbycount(locdata,i)
    N1 = sortbycount(namedata,i)
    F = np.append(F,F1[:3,0])
    L = np.append(L,L1[:3,8])
    N = np.append(N,N1[:3,0])
    
    print(x)
    print(F1[:3,0],N1[:3,0],L1[:3,0])

sampledata = np.column_stack((F,L,N))


np.savetxt('testdata.csv',sampledata, delimiter=",", fmt='%s')