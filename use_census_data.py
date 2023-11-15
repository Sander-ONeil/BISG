import numpy as np

surname = 'oneil'
surname = surname.upper()
zipcode = '10475'

import os

def load_data(file_name):
    data = np.loadtxt(file_name, delimiter=",", dtype=str)
    return data

file_name ='census_name_data_rank_1_100000.csv'
namedata = load_data(file_name)

print(namedata.shape)
nheader = namedata[0,:]
print(nheader)
namedata = namedata[1:namedata.shape[0]]

locdata = load_data('census_loc_data_same_format.csv')[1:,1:]
print(locdata.shape)
lheader = locdata[0,:]
print(lheader)
locdata = locdata[1:locdata.shape[0]]

print(locdata[:,8])

n_i = np.argwhere(namedata[:,0] == surname)[0][0]
l_i = np.argwhere(locdata[:,8] == zipcode)[0][0]

N = namedata[n_i]
N[N=='(S)'] = '0'
print(n_i,l_i)
print(nheader)
print(N)
np.argwhere((namedata[:,3]) == 100)

#print(lheader)

print(locdata[l_i])

for h,n,l in zip(nheader,N,locdata[l_i]):
    a = ' '*20
    print(h,a[0:(20-len(h))],n,a[0:(20-len(n))],l)
    


Totals = np.array([["NAME","DP1_0076C","DP1_0084P","DP1_0080P","DP1_0082P","DP1_0079P","DP1_0093P","DP1_0078P","us"],
["United States","331449281","4.08779979","0.67934949","6.10673734","12.05021108","18.72987741","57.83619335","1"]])




Races = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7}




def bad_method(p_race_giv_loc,p_race_giv_name):
    return (p_race_giv_loc+p_race_giv_name)/2

Probs = {}
bad_Probs = {}

T1 = 0
for x in Races:
    i = Races[x]
    T1 += float(N[i])
    
print('Totals N: ', T1)
T1 = min(100,T1)
N =  np.append(N,str(100-T1))


T1 = 0
for x in Races:
    i = Races[x]
    T1 += float(locdata[l_i][i])
print('Totals L: ', T1)
T1 = min(100,T1)
L = np.append(locdata[l_i],str(100-T1))
L[9] = str(100-T1)

T1 = 0
for x in Races:
    i = Races[x]
    T1 += float(Totals[1,i])
print('Totals T: ', T1)
T1 = min(100,T1)
T = np.append(Totals[1],str(100-T1))
print(T[9],L[9],N[9])



# # Given probabilities
# p_race_giv_loc = Probability someone is race given they're from loc
# p_race_giv_name =  Probability someone is race given they're named name
# p_loc = Prior probability someone is from loc
# p_name = Prior probability someone is named name


def p_namelocandrace(p_race_giv_loc,p_race_giv_name,p_loc,p_name,p_race):
    # Compute the probability someone is from loc given they're Race
    p_loc_giv_race = p_race_giv_loc * p_loc / p_race

    # Compute the probability someone is named name given they're Race
    p_name_giv_race = (p_race_giv_name * p_name) / (p_race)

    #(ESTIMATE) prob that someone is named name and from loc given Race
    p_nameandloc_giv_race = p_loc_giv_race*p_name_giv_race
    
    return p_nameandloc_giv_race*p_race


def P_Race(p_race_giv_loc,p_race_giv_name,p_loc,p_name,p_race,p_nameANDlocation):

    # Final propability that someone is the race given they are from loc and have name
    P_race_giv_nameandloc = p_namelocandrace(p_race_giv_loc,p_race_giv_name,p_loc,p_name,p_race)/p_nameANDlocation
    
    return P_race_giv_nameandloc

Total_prob = 0
Races_with_other = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7,"Other":9}

p_nameANDlocation = 0

for x in Races_with_other.keys():
    i = Races_with_other[x]
    p_race_giv_loc = float(L[i])/100
    p_race_giv_name = float(N[i])/100
    p_loc = float(L[1]) / float(T[1])
    p_name =float( N[1]) / float(T[1])
    p_a = float(T[i]) / 100
    
    p_nameANDlocation += p_namelocandrace(p_race_giv_loc,p_race_giv_name,p_loc,p_name,p_a)


for x in Races_with_other.keys():
    i = Races_with_other[x]
    p_race_giv_loc = float(L[i])/100
    p_race_giv_name = float(N[i])/100
    p_loc = float(L[1]) / float(T[1])
    p_name =float( N[1]) / float(T[1])
    p_a = float(T[i]) / 100
 
    P = P_Race(p_race_giv_loc,p_race_giv_name,p_loc,p_name,p_a,p_nameANDlocation)
    Probs[x] = P
    
    Total_prob += P
    bad_Probs[x] = bad_method(p_race_giv_loc,p_race_giv_name)



print('probs',Probs)
print('Total prob',Total_prob)

import matplotlib.pyplot as plt

# Creating a figure for the subplot
fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns

# First Pie chart for 'Probs'
axs[0].pie(Probs.values(), labels=Probs.keys(), startangle=90)
axs[0].set_title('Probs')

# Second Pie chart for 'bad_Probs'
axs[1].pie(bad_Probs.values(), labels=bad_Probs.keys(), startangle=90)
axs[1].set_title('bad_Probs')

# Adjust the layout to make room for the legend
plt.tight_layout()

# Display the plot
plt.show()
