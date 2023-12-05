import numpy as np
# Given probabilities
p_a_giv_ev1 = 0.52   # Probability someone is white given they're from NY
p_a_giv_ev2 = 0.733  # Probability someone is white given they're named smith
p_ev1 = 19.84/332    # Prior probability someone is from NY
p_ev2 = 2.5/332     # Prior probability someone is named smith

p_a = 251.6/332 # probability someone is white in entire US


# # Given probabilities
# p_a_giv_ev1 = 0.52   # Probability someone is white given they're from NY
# p_a_giv_ev2 = 0.733  # Probability someone is white given they're named smith
# p_ev1 = 19.84/332    # Prior probability someone is from NY
# p_ev2 = 2.5/332     # Prior probability someone is named smith

# p_a = .05 # probability someone is white in entire US


print('p_w',p_a)

# Compute the probability someone is from NY given they're white
p_ev1_giv_a = p_a_giv_ev1 * p_ev1 / p_a
print(f"Probability someone is from NY given they are white: {p_ev1_giv_a:.4f}")

# Compute the probability someone is from NY given they're not white
np_ev1_giv_a = (1-p_a_giv_ev1) * p_ev1 / (1-p_a)


# Compute the probability someone is named smith given they're white
p_ev2_giv_a = (p_a_giv_ev2 * p_ev2) / (p_a)
print(f"Probability someone is named Smith given they are white: {p_ev2_giv_a:.4f}")

np_ev2_giv_a = (1-p_a_giv_ev2) * p_ev2 / (1-p_a)


p_name_and_location = .114/332

print(p_ev2)

# prob that someone is named smith and from ny given white
p_rev = p_ev1_giv_a*p_ev2_giv_a
print('rev',p_rev)

np_rev = np_ev1_giv_a*np_ev2_giv_a
print('nprev',np_rev)

tot =p_rev*p_a +np_rev*(1-p_a)
print('tot',tot,p_name_and_location)

# p_rev /= tot / p_name_and_location

# np_rev /= tot / p_name_and_location
print('rev',p_rev)

print('nprev',np_rev)

p_name_and_location = p_rev*p_a + np_rev*(1-p_a) #This could be found by itself just how many people are named smith and live in NY

P = p_rev/p_name_and_location*p_a

print(P)

# white NY smith

# 000,  S,  N,  SN,  W,  WS,  WN, WSN
#   0   1   2    3   4    5    6    7

A = np.array([
    [1,1,1,1,1,1,1,1],
    [0,0,0,0,1,1,1,1],
    
    [0,0,1,1,0,0,1,1],
    [0,1,0,1,0,1,0,1],
    
    
    [0,0,0,0,0,0,1,1],
    [0,0,0,0,0,1,0,1],
    
    [0,0,0,1,0,0,0,1],
    [0,0,0,0,0,0,0,1],
    ],dtype = np.float64)

B = np.array([
    332,
    p_a*332,
    
    p_ev1*332,
    p_ev2*332,
    
    
    p_ev1*332*p_a_giv_ev1,
    p_ev2*332*p_a_giv_ev2,
    
    .114,
    .114*0.48728,
    ],dtype = np.float64)

print(np.dot(np.linalg.inv(A),B))
G = np.dot(np.linalg.inv(A),B)*1000000
for x in G :
    xs = str(round(x))
    l = len(xs)
    for a in range(10-l):
        xs = ' '+xs
    
    print(xs)


import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Assuming values for p_a, p_a_giv_ev1, p_a_giv_ev2, p_ev1, and p_ev2 are already defined

# ... [Your matrix calculations here] ...

# Extract results from G
S = G[1]
N = G[2]
W = G[4]
WS = G[5]
WN = G[6]
SN = G[3]
WSN = G[7]

# Subtract overlaps
only_S = S - WS - SN + WSN
only_N = N - WN - SN + WSN
only_W = W - WS - WN + WSN
only_WS = WS - WSN
only_WN = WN - WSN
only_SN = SN - WSN

# Create Venn diagram
venn3(subsets=(round(S),round( N),round( SN),round( W),round( WS),round( WN),round( WSN)), set_labels=('Smith', 'NY', 'White'))
plt.show()
