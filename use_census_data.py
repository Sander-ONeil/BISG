import numpy as np

surname = 'meehan'
surname = surname.upper()
zipcode = '00601'

import os

def load_data(file_name):
    data = np.loadtxt(file_name, delimiter=",", dtype=str)
    return data

namedata = load_data('census_name_data_rank_1_100000.csv')
nheader = namedata[0,:]
namedata = namedata[1:namedata.shape[0]]

locdata = load_data('census_loc_data_same_format.csv')[1:,1:]
lheader = locdata[0,:]
locdata = locdata[1:locdata.shape[0]]

Totals = np.array([["NAME","DP1_0076C","DP1_0084P","DP1_0080P","DP1_0082P","DP1_0079P","DP1_0093P","DP1_0078P","us"],
["United States","331449281","4.08779979","0.67934949","6.10673734","12.05021108","18.72987741","57.83619335","1"]])

#searching for relevant entries
n_i = np.argwhere(namedata[:,0] == surname)[0][0]
l_i = np.argwhere(locdata[:,8] == zipcode)[0][0]

#making singular entries 0
namedata[n_i][namedata[n_i]=='(S)'] = '0'


#following code finds other (as in percent of people not categorized as anything else)
def calculate_others(data):
    races = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7}
    total = sum(float(data[races[x]]) for x in races)
    total = min(100, total)
    other_percentage = 100 - total
    return np.append(data, str(other_percentage)), str(other_percentage)

# Assuming 'Races', 'N', 'locdata', 'l_i', and 'Totals' are predefined
# Calculate 'other' for N
N, other_N = calculate_others(namedata[n_i])

# Calculate 'other' for L
L, other_L = calculate_others(locdata[l_i])

# Calculate 'other' for T
T, other_T = calculate_others(Totals[1])

Races_with_other = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7,"Other":9}
s1 = 'Race'
s2 = 'Name'
s3 = 'Loc'
s4 = 'US total'
print('\n',s1,' '*(30-len(s1)),s2,' '*(30-len(s2)),s3,' '*(30-len(s3)),s4)
for h in Races_with_other:
    i = Races_with_other[h]
    n,l,t = (N[i],L[i],T[i])

    print(h,' '*(30-len(h)),n,' '*(30-len(n)),l,' '*(30-len(l)),t)

# # Given probabilities
# p_race_giv_loc = Probability someone is race given they're from loc
# p_race_giv_name =  Probability someone is race given they're named name
# p_loc = Prior probability someone is from loc
# p_name = Prior probability someone is named name
def bad_method(p_race_giv_loc,p_race_giv_name):
    return (p_race_giv_loc+p_race_giv_name)/2

def p_namelocandrace(p_race_giv_loc,p_race_giv_name,p_loc,p_name,p_race):
    # Compute the probability someone is from loc given they're Race
    p_loc_giv_race = p_race_giv_loc * p_loc / p_race

    # Compute the probability someone is named name given they're Race
    p_name_giv_race = (p_race_giv_name * p_name) / (p_race)

    #(ESTIMATE) prob that someone is named name and from loc given Race
    p_nameandloc_giv_race = p_loc_giv_race*p_name_giv_race
    
    return p_nameandloc_giv_race*p_race

p_nameANDlocation = 0
Total_prob = 0
Probs = {}
bad_Probs = {}
p_namelocandrace_dict = {}
p_loc = float(L[1]) / float(T[1])
p_name =float( N[1]) / float(T[1])

for x in Races_with_other.keys():
    i = Races_with_other[x]
    p_race_giv_loc = float(L[i]) / 100
    p_race_giv_name = float(N[i]) / 100
    p_race = float(T[i]) / 100
    p_namelocandrace_dict[x] =  p_namelocandrace(p_race_giv_loc,p_race_giv_name,p_loc,p_name,p_race)
    p_nameANDlocation += p_namelocandrace_dict[x]
    bad_Probs[x] = bad_method(p_race_giv_loc,p_race_giv_name)

for x in Races_with_other.keys():
    # Final propability that someone is the race given they are from loc and have name
    P = p_namelocandrace_dict[x]/p_nameANDlocation
    Probs[x] = P
    Total_prob += P

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
