import numpy as np

surname = 'Oneil'
surname = surname.upper()
zipcode = '10027'

# using loadtxt()
N = 100000
namedata = np.loadtxt('census_data_rank_1:100000.csv',
                 delimiter=",", dtype=str)
print(namedata.shape)
nheader = namedata[0,:]
print(nheader)
namedata = namedata[1:namedata.shape[0]]

locdata = np.loadtxt('census_loc_data.csv',
                 delimiter=",", dtype=str)
print(locdata.shape)
lheader = locdata[0,:]
print(lheader)
locdata = locdata[1:locdata.shape[0]]

print(locdata[:,8])

n_i = np.argwhere(namedata[:,0] == surname)[0][0]
l_i = np.argwhere(locdata[:,8] == zipcode)[0][0]


print(n_i,l_i)
print(nheader)
print(namedata[n_i])

#print(lheader)

print(locdata[l_i])

for h,n,l in zip(nheader,namedata[n_i],locdata[l_i]):
    a = ' '*20
    print(h,a[0:(20-len(h))],n,a[0:(20-len(n))],l)