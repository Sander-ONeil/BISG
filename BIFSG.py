import numpy as np
import os

def BISFG_func(fname,surname,zipcode,plot = True):
    # searching for relevant entries according to personal data
    n_i = np.argwhere(namedata[:,0] == surname)[0][0]
    l_i = np.argwhere(locdata[:,8] == zipcode)[0][0]
    f_i = np.argwhere(fnamedata[:,0] == fname)[0][0]
    
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
    
    # Calculate 'other' for F
    F, other_F = calculate_others(fnamedata[f_i])
    
    Races_with_other = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7,"Other":9}
    # #printing given race data for Name Loc  and Total, could make this more pie charts
    s1 = 'Race'
    s2 = 'Name'
    s3 = 'Loc'
    s4 = 'US total'
    #print('\n',s1,' '*(30-len(s1)),s2,' '*(30-len(s2)),s3,' '*(30-len(s3)),s4)
    for h in Races_with_other:
        i = Races_with_other[h]
        n,l,t = (N[i],L[i],T[i])
    
        #print(h,' '*(30-len(h)),n,' '*(30-len(n)),l,' '*(30-len(l)),t)
    
    # # Given probabilities
    # p_race_giv_loc = Probability someone is race given they're from loc
    # p_race_giv_name =  Probability someone is race given they're named name
    # p_loc = Prior probability someone is from loc
    # p_name = Prior probability someone is named name
    
    # niave approach
    def bad_method(p_race_giv_loc,p_race_giv_name):
        return (p_race_giv_loc+p_race_giv_name)/2
    
    def p_namelocandrace(p_race_giv_loc,p_race_giv_name,p_race_giv_fname,p_loc,p_name,p_fname,p_race):
        # Compute the probability someone is from loc given they're Race
        p_loc_giv_race = (p_race_giv_loc * p_loc / p_race)
    
        # Compute the probability someone is named name given they're Race
        p_name_giv_race = (p_race_giv_name * p_name) / (p_race)
    
        # Compute the probability someone is fnamed fname given they're Race
        p_fname_giv_race = p_race_giv_fname * p_fname / (p_race)
    
        #(ESTIMATE) prob that someone is named name and from loc given Race
        p_nameandloc_giv_race = p_loc_giv_race*p_name_giv_race*p_fname_giv_race
        
        # returns prob of being of race in loc and having name
        return p_nameandloc_giv_race*p_race
    
    p_nameANDlocation = 0
    Total_prob = 0
    Probs = {}
    bad_Probs = {}
    p_namelocandrace_dict = {}
    p_loc = float(L[1]) / float(T[1])
    p_name = float( N[1]) / float(T[1])
    p_fname = float(F[1]) / total_fname_count
    # loop through races including "other"
    for x in Races_with_other.keys():
        i = Races_with_other[x]
        
        p_race = float(T[i]) / 100
        
        # get probs for race
        p_race_giv_loc = float(L[i]) / 100+0.0000001
        p_race_giv_name = float(N[i]) / 100+0.0000001
        p_race_giv_fname =  float(F[i]) / 100+0.0000001
        
    
    
        # get prob of being race in loc and with name
        p_namelocandrace_dict[x] =  p_namelocandrace(p_race_giv_loc,p_race_giv_name,p_race_giv_fname,p_loc,p_name,p_fname,p_race)
        # add to total
        p_nameANDlocation += p_namelocandrace_dict[x]
        # get niave approach
        bad_Probs[x] = bad_method(p_race_giv_loc,p_race_giv_name)
    
    for x in Races_with_other.keys():
        # Final propability that someone is the race given they are from loc and have name
        P = p_namelocandrace_dict[x]/p_nameANDlocation
        Probs[x] = P
        Total_prob += P

    #print('probs',Probs)
    # print('Total prob',Total_prob)
    
    if plot:
        #plotting BISG results vs niave approach
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
        
        # Create a figure with custom GridSpec for flexible subplot sizes
        fig = plt.figure(figsize=(14, 8))
        gs = gridspec.GridSpec(4, 2, figure=fig,width_ratios=[1, 2], height_ratios=[1, 1, 1,1])
        
        # Define the axes
        ax1 = fig.add_subplot(gs[0:2, 1])  # Probs pie (larger)
        ax2 = fig.add_subplot(gs[2, 1])  # bad_Probs pie
        ax3 = fig.add_subplot(gs[1, 0])  # Surname racial breakdown
        ax4 = fig.add_subplot(gs[2, 0])  # Zipcode racial breakdown
        ax5 = fig.add_subplot(gs[3, 0])  # US total racial breakdown
        ax6 = fig.add_subplot(gs[0, 0])  # First name racial breakdown
         
        colors = [ "#d62728", "#9467bd", "#ff7f0e", "#000000", "#1f77b4", "#c9bfbf", "#17becf"]
        Races_with_other = {"2 Races":2,"Alaskan/American Native":3,"Asian/Pacific Islander":4,"Black":5,"Hispanic":6,"White":7,"Other":9}
        
        
        # Probs pie (larger)
        probs_pie = ax1.pie(Probs.values(), colors=colors)
        ax1.set_title('Probs BISG approach')
        
        # bad_Probs pie
        bad_probs_pie = ax2.pie(bad_Probs.values(), colors=colors)
        ax2.set_title('bad_Probs Naive Approach')
        
        # Given Data pies
        race_ind = list(Races_with_other.values())
        surname_pie = ax3.pie(N[race_ind], colors=colors)
        ax3.set_title(surname + ' racial breakdown')
        
        zipcode_pie = ax4.pie(L[race_ind], colors=colors)
        ax4.set_title(zipcode + ' racial breakdown')
        
        us_total_pie = ax5.pie(T[race_ind], colors=colors)
        ax5.set_title('US total racial breakdown')
        
        fname_pie = ax6.pie(F[race_ind], colors=colors)
        ax6.set_title(fname+' racial breakdown')
        # Add a single legend for all pie charts
        plt.figlegend(probs_pie[0], Races_with_other.keys(), loc='center right',)
        
        # Adjust the layout to accommodate the legend and ensure no overlap
        # fig.tight_layout()
        fig.subplots_adjust(right=0.85)
        
        # Display the plot
        plt.show()

    
    return (Probs,bad_Probs)
    

    

#loading data from csv into numpy
def load_data(file_name):
    data = np.loadtxt( os.path.dirname(os.path.abspath(__file__))+'/'+file_name, delimiter=",", dtype=str)
    return data

namedata = load_data('census_name_data_rank_1_100000.csv')
nheader = namedata[0,:]
namedata = namedata[1:namedata.shape[0]]

# this data is wierdly formatted so it takes of first column and row; could solve but would have to change multiple files in github
locdata = load_data('census_loc_data_same_format.csv')[1:,1:]
lheader = locdata[0,:]
locdata = locdata[1:locdata.shape[0]]


fnamedata = load_data('fnamedata.csv')
fheader = fnamedata[0,:]
fnamedata = fnamedata[1:fnamedata.shape[0]]
total_fname_count = np.sum(fnamedata[:,1].astype(float))
#print(fnamedata.shape)
#print(total_fname_count) #name count lower than total pop significantly. Should use this to get prob I think, depends if its representative sample, if every instance of these names are counted then could divide by us pop

# total data for US
Totals = np.array([["NAME","DP1_0076C","DP1_0084P","DP1_0080P","DP1_0082P","DP1_0079P","DP1_0093P","DP1_0078P","us"],
["United States","331449281","4.08779979","0.67934949","6.10673734","12.05021108","18.72987741","57.83619335","1"]])



# data of person to examine
fname = 'RYAN'
fname = fname.upper()
surname = 'pRICE'
# surname = 'ARREZ'
surname = surname.upper()

zipcode = '14204'
# zipcode = '35185'

Probs,bad_Probs = BISFG_func(fname,surname,zipcode,plot = True)
g_mas_order = ['White','Black','API','AIAN','Multi','Hisp','Other']