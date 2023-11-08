import numpy as np

surname = 'WASHINGTON'
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

locdata = np.loadtxt('census_loc_data_same_format.csv',
                 delimiter=",", dtype=str)[1:,1:]
print(locdata.shape)
lheader = locdata[0,:]
print(lheader)
locdata = locdata[1:locdata.shape[0]]

print(locdata[:,8])

n_i = np.argwhere(namedata[:,0] == surname)[0][0]
l_i = np.argwhere(locdata[:,9] == zipcode)[0][0]


print(n_i,l_i)
print(nheader)
print(namedata[n_i])

#print(lheader)

print(locdata[l_i])

for h,n,l in zip(nheader,namedata[n_i],locdata[l_i]):
    a = ' '*20
    print(h,a[0:(20-len(h))],n,a[0:(20-len(n))],l)
    
    

Totals = np.array([["NAME","DP1_0076C","DP1_0084P","DP1_0080P","DP1_0082P","DP1_0079P","DP1_0093P","DP1_0078P","us"],
["United States","331449281","4.08779979","0.67934949","6.10673734","12.05021108","18.72987741","57.83619335","1"]])


Races = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7}


    

def P_Race(p_a_giv_ev1,p_a_giv_ev2,p_ev1,p_ev2,p_a):
    # # Given probabilities
    # p_a_giv_ev1 = 0.52   # Probability someone is white given they're from NY
    # p_a_giv_ev2 = 0.733  # Probability someone is white given they're named smith
    # p_ev1 = 19.84/332    # Prior probability someone is from NY
    # p_ev2 = 2.5/332     # Prior probability someone is named smith
    
    # p_a = .05 # probability someone is white in entire US
    
    
    # print('p_w',p_a)
    
    # Compute the probability someone is from NY given they're white
    p_ev1_giv_a = p_a_giv_ev1 * p_ev1 / p_a
    # print(f"Probability someone is from NY given they are white: {p_ev1_giv_a:.4f}")
    
    # Compute the probability someone is from NY given they're not white
    np_ev1_giv_a = (1-p_a_giv_ev1) * p_ev1 / (1-p_a)
    
    
    # Compute the probability someone is named smith given they're white
    p_ev2_giv_a = (p_a_giv_ev2 * p_ev2) / (p_a)
    # print(f"Probability someone is named Smith given they are white: {p_ev2_giv_a:.4f}")
    
    np_ev2_giv_a = (1-p_a_giv_ev2) * p_ev2 / (1-p_a)
    
    
    p_name_and_location = 0.144/332
    
    # print(p_ev2)
    
    # prob that someone is named smith and from ny given white
    p_rev = p_ev1_giv_a*p_ev2_giv_a
    pr = p_ev1_giv_a*p_name_and_location/p_ev1
    
    # print('rev',p_rev,pr)
    
    np_rev = np_ev1_giv_a*np_ev2_giv_a
    # print('nprev',np_rev)
    
    tot =p_rev*p_a +np_rev*(1-p_a)
    # print('tot',tot,p_name_and_location)
    
    p_rev /= tot / p_name_and_location
    
    np_rev /= tot / p_name_and_location
    # print('rev',p_rev)
    
    # print('nprev',np_rev)
    
    p_name_and_location = p_rev*p_a + np_rev*(1-p_a) #This could be found by itself just how many people are named smith and live in NY
    
    P = p_rev/p_name_and_location*p_a

    return P

def bad_method(p_a_giv_ev1,p_a_giv_ev2):
    return (p_a_giv_ev1+p_a_giv_ev2)/2

Probs = {}
bad_Probs = {}
N = namedata[n_i]
L = locdata[l_i]
T = Totals[1]
Total_prob = 0
for x in Races.keys():
    i = Races[x]
    p_a_giv_ev1 = float(L[i])/100
    print('Probability someone is ' + x + ' given they\'re from ' + L[0]+': ' + str(p_a_giv_ev1))
    p_a_giv_ev2 = float(N[i])/100
    print('Probability someone is ' + x + ' given they\'re named ' + N[0]+': ' + str(p_a_giv_ev2))
    p_ev1 = float(L[1]) / float(T[1])
    print('Probability someone is from ' + L[0] + " :" + str(p_ev1))
    p_ev2 =float( N[1]) / float(T[1])
    print('Probability someone is Named ' + N[0] + " :" + str(p_ev2))
    
    p_a = float(T[i]) / 100
    
    print('Probability someone is ' + x + " :" + str(p_a))
    # p_a_giv_ev1 = Probability someone is race given they're from loc
    # p_a_giv_ev2 =  Probability someone is race given they're named name
    # p_ev1 =  Prior probability someone is from loc
    # p_ev2 =  Prior probability someone is named name
    P = P_Race(p_a_giv_ev1,p_a_giv_ev2,p_ev1,p_ev2,p_a)
    
    print('\n Probability someone is ' + x + 'given both '+str(P))
    
    print('\n\n')
    Probs[x] = P
    Total_prob += P
    bad_Probs[x] = bad_method(p_a_giv_ev1,p_a_giv_ev2)
print(Total_prob)

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