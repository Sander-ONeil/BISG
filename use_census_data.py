import numpy as np

surname = 'oneil'
surname = surname.upper()
zipcode = '14228'

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


   
def amount_of_people_with_name_in_loc(p_a_giv_ev1,p_a_giv_ev2,p_ev1,p_ev2,p_a):

    p_ev1_giv_a = p_a_giv_ev1 * p_ev1 / p_a

    # Compute the probability someone is from loc given they're not Race
    np_ev1_giv_a = (1-p_a_giv_ev1) * p_ev1 / (1-p_a)
    
    
    # Compute the probability someone is named name given they're Race
    p_ev2_giv_a = (p_a_giv_ev2 * p_ev2) / (p_a)
    np_ev2_giv_a = (1-p_a_giv_ev2) * p_ev2 / (1-p_a)
    
    
    p_rev = p_ev1_giv_a*p_ev2_giv_a
    np_rev = np_ev1_giv_a*np_ev2_giv_a

    
    return (p_rev*p_a+np_rev*(1-p_a))*331449281
 


def P_Race(p_a_giv_ev1,p_a_giv_ev2,p_ev1,p_ev2,p_a):
    # # Given probabilities
    # p_a_giv_ev1 = Probability someone is race given they're from loc
    # p_a_giv_ev2 =  Probability someone is race given they're named name
    # p_ev1 =  Prior probability someone is from loc
    # p_ev2 =     Prior probability someone is named name
    p_name_and_location = p_ev1*p_ev2
    # Compute the probability someone is from loc given they're Race
    p_ev1_giv_a = p_a_giv_ev1 * p_ev1 / p_a

    # Compute the probability someone is from loc given they're not Race
    np_ev1_giv_a = (1-p_a_giv_ev1) * p_ev1 / (1-p_a)
    
    
    # Compute the probability someone is named name given they're Race
    p_ev2_giv_a = (p_a_giv_ev2 * p_ev2) / (p_a)
    np_ev2_giv_a = (1-p_a_giv_ev2) * p_ev2 / (1-p_a)
    
    # print('prob from loc ',p_ev1*331449281,'prob from loc and race',p_ev1_giv_a*331449281*p_a,'\n inv',(np_ev1_giv_a)*331449281*(1-p_a))
    
    
    
    
    # print('prob name ',p_ev2*331449281,'prob from name and race',p_ev2_giv_a*331449281*p_a,'\n inv',(np_ev2_giv_a)*331449281*(1-p_a))
    
    
    # prob that someone is named name and from loc given Race
    p_rev = p_ev1_giv_a*p_ev2_giv_a
    np_rev = np_ev1_giv_a*np_ev2_giv_a
    
    tot =p_rev*p_a +np_rev*(1-p_a)
    print('tot',tot*331449281,p_name_and_location*331449281)
    
    p_rev /= tot / p_name_and_location
    
    np_rev /= tot / p_name_and_location
    # print('prob from loc and name',p_name_and_location*331449281,'prob from loc name and race',p_rev*331449281*p_a,np_rev*331449281*(1-p_a))
    tot =p_rev*p_a +np_rev*(1-p_a)
    print('tot',tot*331449281,p_name_and_location*331449281)
    
    
    # print('\n\nnew ',p_a_giv_ev1*p_a_giv_ev2*p_name_and_location*331449281,'\nold ',p_rev*331449281*p_a,'\ntotal ',p_name_and_location*331449281)
    
    # print('\n number of people with name in loc according to group',amount_of_people_with_name_in_loc(p_a_giv_ev1,p_a_giv_ev2,p_ev1,p_ev2,p_a))
    
    # p_rev = p_a_giv_ev1*p_a_giv_ev2*p_name_and_location/p_a
    
    #(p_rev*p_a+np_rev*(1-p_a)) = p_name_and_location
    
    #print('prob that someone is named name and from loc given Race',p_rev)
    
    
    # 000,  N,  L,  NL,  R,  RN,  RL, RNL,
    #   0   1   2    3   4    5    6    7
    
    # A = np.array([
    #     [1,1,1,1,1,1,1,1],
    #     [0,0,0,0,1,1,1,1],
        
    #     [0,0,1,1,0,0,1,1],
    #     [0,1,0,1,0,1,0,1],
        
        
    #     [0,0,0,0,0,0,1,1],
    #     [0,0,0,0,0,1,0,1],
        
    #     [0,0,0,1,0,0,0,1],
    #     [0,0,0,0,0,0,0,1],
    #     ],dtype = np.float64)
    
    
    
    
    P = p_rev*p_a/(p_rev*p_a+np_rev*(1-p_a))
    
    # B = np.array([
    #     331449281,
    #     p_a*331449281,
        
    #     p_ev1*331449281,
    #     p_ev2*331449281,
        
        
    #     p_ev1_giv_a*p_a*331449281,
    #     p_ev2*331449281*p_a_giv_ev2,
        
    #     331449281*p_name_and_location,
    #     p_name_and_location*331449281*P,
    #     ],dtype = np.float64)
    # G = np.dot(np.linalg.inv(A),B)
    
    # print(np.dot(np.linalg.inv(A),B))
    
    return P

def bad_method(p_a_giv_ev1,p_a_giv_ev2):
    return (p_a_giv_ev1+p_a_giv_ev2)/2

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
Total_prob = 0
people_with_name = 0

# Races = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7,"Other":9}
Races_with_other = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7,"Other":9}
for x in Races_with_other.keys():
    print('\n\n')
    print(x,'\n')
    i = Races_with_other[x]
    p_a_giv_ev1 = float(L[i])/100
    # print('Probability someone is ' + x + ' given they\'re from ' + L[0]+': ' + str(p_a_giv_ev1))
    p_a_giv_ev2 = float(N[i])/100
    # print('Probability someone is ' + x + ' given they\'re named ' + N[0]+': ' + str(p_a_giv_ev2))
    p_ev1 = float(L[1]) / float(T[1])
    # print('Probability someone is from ' + L[0] + " :" + str(p_ev1))
    p_ev2 =float( N[1]) / float(T[1])
    # print('Probability someone is Named ' + N[0] + " :" + str(p_ev2))
    
    p_a = float(T[i]) / 100
    
    # print('Probability someone is ' + x + " :" + str(p_a))
    # p_a_giv_ev1 = Probability someone is race given they're from loc
    # p_a_giv_ev2 =  Probability someone is race given they're named name
    # p_ev1 =  Prior probability someone is from loc
    # p_ev2 =  Prior probability someone is named name
    P = P_Race(p_a_giv_ev1,p_a_giv_ev2,p_ev1,p_ev2,p_a)
    
    # print('\n Probability someone is ' + x + 'given both '+str(P))
    
    
    nP = P_Race(1-p_a_giv_ev1,1-p_a_giv_ev2,p_ev1,p_ev2,1-p_a)
    # print('inv probs',1-p_a_giv_ev1,1-p_a_giv_ev2,p_ev1,p_ev2,1-p_a)
    
    print('prob and rev',P,'  :  ',nP,' = ',P+nP)
    Probs[x] = P
    Total_prob += P
    bad_Probs[x] = bad_method(p_a_giv_ev1,p_a_giv_ev2)
    
    people_with_name += P*amount_of_people_with_name_in_loc(p_a_giv_ev1,p_a_giv_ev2,p_ev1,p_ev2,p_a)

print('people with name simple',p_ev1*p_ev2*331449281)
print('people_With_name',people_with_name,people_with_name/Total_prob)
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
