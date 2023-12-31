from BIFSG import *



g_mas_order = ['White','Black','API','AIAN','Multi','Hisp','Other']



Races = {"2 Races":4,"Alaskan/American Native":3,"Asian/Pacific Islander":2,"Black":1,"Hispanic":5,"White":0,"Other":6}
        

Tdata = np.loadtxt( os.path.dirname(os.path.abspath(__file__))+'/'+'Truth_data.csv',
                 delimiter=",", dtype=str,usecols = range(0,11))


tvector = np.array(Tdata[1:,4:11],dtype = float)#accepted truth

print(Tdata)
Pvector = tvector*0
Bvector = tvector*0
Worst = tvector*0
Worst[:,0] = 1

i = 0
for r in Tdata[1:]:
    fname = r[0]
    surname = r[1]
    zipcode = '0'*(5-len(r[2])) + r[2]
    
    # print(fname,surname,zipcode)
    
    Probs,bad_Probs = BISFG_func(fname,surname,zipcode,plot = False,correcting=False)
    for race in Races:
        Pvector[i,Races[race]] = Probs[race]
        Bvector[i,Races[race]] = bad_Probs[race]
    # print(Pvector[i])
    i+=1
    # print('*******************')
    

import matplotlib.pyplot as plt
import matplotlib.colors
#import seaborn as sns

races = ['White','Black','API','AIAN','Multi','Hisp','Other']

N = 256
vals = np.ones((N, 4))
vals[:, 0] = np.linspace(0, 0, N)
vals[:, 1] = np.linspace(0, 0, N)
vals[:, 2] = np.linspace(0/256, 1, N)
newcmp = matplotlib.colors.ListedColormap(vals)


def confusion_plot(A, l, f):
    f.imshow(A, interpolation='nearest', cmap=newcmp)
    
    f.set_xlabel('Predicted labels')
    f.set_ylabel('True labels')

    
    f.set_xticks(range(A.shape[0]), l)
    f.set_yticks(range(A.shape[1]), l)
    
    

    # Loop over data dimensions and create text annotations.
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            text = f.text(j, i, A[i, j],
                           ha="center", va="center", color="white",fontsize = 40)





def confusion(T, P,title='None'):
    t = np.argmax(T, axis=1)
    p = np.argmax(P, axis=1)
    
    
    
    # Plot for each race
    fig, axs = plt.subplots(4, 2, figsize=(10, 20))  # Adjust the layout as needed
    axs = axs.flatten()
    
    for x, r in enumerate(races):
        pp = p == x
        pn = pp == False
        tp = t == x
        tn = tp == False

        TP = np.sum(pp & tp)
        FP = np.sum(pp & tn)
        TN = np.sum(pn & tn)
        FN = np.sum(pn & tp)

        c = np.array([[TP, FP], [FN, TN]])

        confusion_plot(c,['True','False'],axs[x])
        axs[x].set_title(r)
    plt.title('Confusion matrixes '+title)
    
    
    
    plt.tight_layout()
    
    multiclass = np.zeros((7,7),dtype = int)
    
    indices = np.column_stack((t,p))
    print(indices)
    for i in indices:
        multiclass[i[1],i[0]] += 1
    
    fig, axs = plt.subplots(1, 1, figsize=(10, 10))
    #axs = axs.flatten()
    confusion_plot(multiclass,races,axs)
    plt.title('Multi-class Confusion Matrix '+title)
    
    #plt.show()



    
distP = np.sum(abs(Pvector-tvector),axis = 1)
distB = np.sum(abs(Bvector-tvector),axis = 1)
distW = np.sum(abs(Worst-tvector),axis = 1)
r = Tdata[24]
fname = r[0]
surname = r[1]
zipcode = r[2]

#Probs,bad_Probs = BISFG_func(fname,surname,zipcode,plot = True)

print('sum of error worst: ',np.sum(Worst))
print('sum of error bad: ',np.sum(distB))
print('sum of error: ',np.sum(distP))

C = confusion(Pvector,tvector, 'BIFSG method')
Cb = confusion(Bvector,tvector,'Bad Pred')
plt.show()
#print(C)


P = np.argmax(Pvector, axis=1)
T = np.argmax(tvector, axis=1)
B = np.argmax(Bvector, axis=1)
W = np.argmax(Worst,axis = 1)
Y = np.sum((P == T))
N = np.sum((P == T)==False)


wrong = np.argwhere((P == T)==False)
print(wrong)

for w in wrong:
    w = w[0]
    # print(Tdata[w+1])
    print('predicted',races[P[w]],end=',')
    # print(Pvector[w])
    print('true',races[T[w]],': ',Tdata[w+1][2])
    
    #print(Tdata[w+1][2],end = ', ')
    
    

print('correct' , Y , ' out of ', Y+N)
print('bad method ', np.sum((B == T)), 'out of ', np.sum((B == T)==False) + np.sum((B == T)))
print('worst method ', np.sum((W == T)), 'out of ', np.sum((W == T)==False) + np.sum((W == T)))






#plotting BISG results vs niave approach
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Create a figure with custom GridSpec for flexible subplot sizes
fig = plt.figure(figsize=(14, 8))
gs = gridspec.GridSpec(1, 3, figure=fig,width_ratios=[1, 1, 1,], height_ratios=[1,])

# Define the axes
ax1 = fig.add_subplot(gs[0, 0])  # Probs pie (larger)
ax2 = fig.add_subplot(gs[0, 1])  # bad_Probs pie
ax3 = fig.add_subplot(gs[0, 2])  # Surname racial breakdown

colors = [ "green", "red", "#ff7f0e", "#000000", "#1f77b4", "#c9bfbf", "#17becf"]

#fig.set_title('Correct identifications of test data')
# Probs pie (larger)
P_pie = ax1.pie([Y,N], colors=colors)
ax1.set_title('Probs BISG approach')

# bad_Probs pie
B_pie = ax2.pie([np.sum((B == T)),np.sum((B == T)==False)], colors=colors)
ax2.set_title('bad_Probs Naive Approach')

# Given Data pies

W_pie = ax3.pie([np.sum((W == T)),np.sum((W == T)==False)], colors=colors)
ax3.set_title('Worst approach')

# Add a single legend for all pie charts
plt.figlegend(P_pie[0], ['True','False'], loc='center right',)


fig.subplots_adjust(right=0.85)

# Display the plot
plt.show()


total_prob =  [np.sum(tvector,axis = 0),np.sum(Pvector,axis = 0),np.sum(Bvector,axis = 0),np.sum(Worst,axis=0)]

for t in range(len(total_prob)):

    total_prob[t] = total_prob[t]/np.linalg.norm(total_prob[t])

print(total_prob)


# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))
 

 
# Set position of bar on X axis
br1 = np.arange(len(total_prob[0]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
 

# Make the plot
plt.bar(br1, total_prob[0], color ='r', width = barWidth,
        edgecolor ='grey', label ='Truth')
plt.bar(br2, total_prob[1], color ='g', width = barWidth,
        edgecolor ='grey', label ='Prediction')
plt.bar(br3, total_prob[2], color ='b', width = barWidth,
        edgecolor ='grey', label ='bad Prediction')
plt.bar(br4, total_prob[3], color ='c', width = barWidth,
        edgecolor ='grey', label ='Worst guess')
 
# Adding Xticks
plt.xlabel('Race', fontweight ='bold', fontsize = 15)
plt.ylabel('Total Proportion', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(total_prob[0]))],
        races)
 
plt.legend()
plt.show()
##############bar chart 2

# total_prob =  [np.sum(T,axis = 0),np.sum(P,axis = 0),np.sum(B,axis = 0),np.sum(W,axis=0)]

# for t in range(len(total_prob)):

#     total_prob[t] = total_prob[t]/np.linalg.norm(total_prob[t])

# print(total_prob)



# # set width of bar
# barWidth = 0.25
# fig = plt.subplots(figsize =(12, 8))
 

 
# # Set position of bar on X axis
# br1 = np.arange(len(total_prob[0]))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]
# br4 = [x + barWidth for x in br3]
 

# # Make the plot
# plt.bar(br1, total_prob[0], color ='r', width = barWidth,
#         edgecolor ='grey', label ='Truth')
# plt.bar(br2, total_prob[1], color ='g', width = barWidth,
#         edgecolor ='grey', label ='Prediction')
# plt.bar(br3, total_prob[2], color ='b', width = barWidth,
#         edgecolor ='grey', label ='bad Prediction')
# plt.bar(br4, total_prob[3], color ='c', width = barWidth,
#         edgecolor ='grey', label ='Worst guess')
 
# # Adding Xticks
# plt.xlabel('Race', fontweight ='bold', fontsize = 15)
# plt.ylabel('Total Proportion', fontweight ='bold', fontsize = 15)
# plt.xticks([r + barWidth for r in range(len(total_prob[0]))],
#         races)
 
# plt.legend()
# plt.show()
################################3



total = np.array([57.83619335,12.05021108,6.10673734,0.67934949,4.08779979,18.72987741,.01])


X = np.arange(-100,200)
Y = np.zeros((300))
print(X.shape,Y.shape)
i = 0
for x in range(-100,200):
    x = x/100
    

    Pvector2 = Pvector / ((total)**x)
    
    P = np.argmax(Pvector2, axis=1)
    print(np.sum((P == T)), 'out of ', np.sum((P == T)==False) + np.sum((P == T)))
    
    Y[i] = np.sum((P == T))/(np.sum((P == T)==False) + np.sum((P == T)))
    i+=1
    

plt.scatter(X/100,Y)
plt.xlabel('Exponent')
plt.ylabel('Accuracy')

plt.title('Dividing by significance (Total US racial breakdown)')
plt.show()

#####################################################################################################
i = 0
for r in Tdata[1:]:
    fname = r[0]
    surname = r[1]
    zipcode = '0'*(5-len(r[2])) + r[2]
    
    # print(fname,surname,zipcode)
    
    Probs,bad_Probs = BISFG_func(fname,surname,zipcode,plot = False,correcting=True)
    for race in Races:
        Pvector[i,Races[race]] = Probs[race]
        Bvector[i,Races[race]] = bad_Probs[race]
    # print(Pvector[i])
    i+=1
    # print('*******************')
    

import matplotlib.pyplot as plt
import matplotlib.colors
#import seaborn as sns

races = ['White','Black','API','AIAN','Multi','Hisp','Other']

N = 256
vals = np.ones((N, 4))
vals[:, 0] = np.linspace(0, 0, N)
vals[:, 1] = np.linspace(0, 0, N)
vals[:, 2] = np.linspace(0/256, 1, N)
newcmp = matplotlib.colors.ListedColormap(vals)


def confusion_plot(A, l, f):
    f.imshow(A, interpolation='nearest', cmap=newcmp)
    
    f.set_xlabel('Predicted labels')
    f.set_ylabel('True labels')

    
    f.set_xticks(range(A.shape[0]), l)
    f.set_yticks(range(A.shape[1]), l)
    
    

    # Loop over data dimensions and create text annotations.
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            text = f.text(j, i, A[i, j],
                           ha="center", va="center", color="white",fontsize = 40)





def confusion(T, P,title='None'):
    t = np.argmax(T, axis=1)
    p = np.argmax(P, axis=1)
    
    
    
    # Plot for each race
    fig, axs = plt.subplots(1, 7, figsize=(30, 10))  # Adjust the layout as needed
    axs = axs.flatten()
    
    for x, r in enumerate(races):
        pp = p == x
        pn = pp == False
        tp = t == x
        tn = tp == False

        TP = np.sum(pp & tp)
        FP = np.sum(pp & tn)
        TN = np.sum(pn & tn)
        FN = np.sum(pn & tp)

        c = np.array([[TP, FP], [FN, TN]])

        confusion_plot(c,['True','False'],axs[x])
        axs[x].set_title(r)
    plt.title('Confusion matrixes '+title)
    
    
    
    plt.tight_layout()
    
    multiclass = np.zeros((7,7),dtype = int)
    
    indices = np.column_stack((t,p))
    print(indices)
    for i in indices:
        multiclass[i[1],i[0]] += 1
    
    fig, axs = plt.subplots(1, 1, figsize=(10, 10))
    #axs = axs.flatten()
    confusion_plot(multiclass,races,axs)
    plt.title('Multi-class Confusion Matrix '+title)
    
    #plt.show()



    
distP = np.sum(abs(Pvector-tvector),axis = 1)
distB = np.sum(abs(Bvector-tvector),axis = 1)
distW = np.sum(abs(Worst-tvector),axis = 1)
r = Tdata[24]
fname = r[0]
surname = r[1]
zipcode = r[2]

#Probs,bad_Probs = BISFG_func(fname,surname,zipcode,plot = True)

print('sum of error worst: ',np.sum(Worst))
print('sum of error bad: ',np.sum(distB))
print('sum of error: ',np.sum(distP))

C = confusion(Pvector,tvector, 'BIFSG method With Correction')
#Cb = confusion(Bvector,tvector,'Bad Pred')
plt.show()
#print(C)
###########ROC










P = np.argmax(Pvector, axis=1)
T = np.argmax(tvector, axis=1)
B = np.argmax(Bvector, axis=1)
W = np.argmax(Worst,axis = 1)
Y = np.sum((P == T))
N = np.sum((P == T)==False)


wrong = np.argwhere((P == T)==False)
print(wrong)

for w in wrong:
    w = w[0]
    # print(Tdata[w+1])
    print('predicted',races[P[w]],end=',')
    # print(Pvector[w])
    print('true',races[T[w]],': ',Tdata[w+1][2])
    
    #print(Tdata[w+1][2],end = ', ')
    
    
    
print('correct' , Y , ' out of ', Y+N)
print('bad method ', np.sum((B == T)), 'out of ', np.sum((B == T)==False) + np.sum((B == T)))

print('worst method ', np.sum((W == T)), 'out of ', np.sum((W == T)==False) + np.sum((W == T)))

total_prob =  [np.sum(tvector,axis = 0),np.sum(Pvector,axis = 0),np.sum(Bvector,axis = 0),np.sum(Worst,axis=0)]

for t in range(len(total_prob)):

    total_prob[t] = total_prob[t]/np.linalg.norm(total_prob[t])

print(total_prob)


# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))
 

 
# Set position of bar on X axis
br1 = np.arange(len(total_prob[0]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
 

# Make the plot
plt.bar(br1, total_prob[0], color ='r', width = barWidth,
        edgecolor ='grey', label ='Truth')
plt.bar(br2, total_prob[1], color ='g', width = barWidth,
        edgecolor ='grey', label ='Prediction')
plt.bar(br3, total_prob[2], color ='b', width = barWidth,
        edgecolor ='grey', label ='bad Prediction')
plt.bar(br4, total_prob[3], color ='c', width = barWidth,
        edgecolor ='grey', label ='Worst guess')
 
# Adding Xticks
plt.xlabel('Race', fontweight ='bold', fontsize = 15)
plt.ylabel('Total Proportion', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(total_prob[0]))],
        races)
 
plt.legend()
plt.show()


#plotting BISG results vs niave approach
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Create a figure with custom GridSpec for flexible subplot sizes
fig = plt.figure(figsize=(14, 8))
gs = gridspec.GridSpec(1, 3, figure=fig,width_ratios=[1, 1, 1,], height_ratios=[1,])

# Define the axes
ax1 = fig.add_subplot(gs[0, 0])  # Probs pie (larger)
ax2 = fig.add_subplot(gs[0, 1])  # bad_Probs pie
ax3 = fig.add_subplot(gs[0, 2])  # Surname racial breakdown

colors = [ "green", "red", "#ff7f0e", "#000000", "#1f77b4", "#c9bfbf", "#17becf"]

#fig.set_title('Correct identifications of test data')
# Probs pie (larger)
P_pie = ax1.pie([Y,N], colors=colors)
ax1.set_title('Probs BISG approach')

# bad_Probs pie
B_pie = ax2.pie([np.sum((B == T)),np.sum((B == T)==False)], colors=colors)
ax2.set_title('bad_Probs Naive Approach')

# Given Data pies

W_pie = ax3.pie([np.sum((W == T)),np.sum((W == T)==False)], colors=colors)
ax3.set_title('Worst approach')

# Add a single legend for all pie charts
plt.figlegend(P_pie[0], ['True','False'], loc='center right',)
plt.show()
