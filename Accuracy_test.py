from BIFSG import *

Probs,bad_Probs = BISFG_func(fname,surname,zipcode,plot = False)
g_mas_order = ['White','Black','API','AIAN','Multi','Hisp','Other']
Races = {"2 Races":4,"Alaskan/American Native":3,"Asian/Pacific Islander":2,"Black":1,"Hispanic":5,"White":0,"Other":6}
        

Tdata = np.loadtxt( os.path.dirname(os.path.abspath(__file__))+'/'+'Truth_data.csv',
                 delimiter=",", dtype=str,usecols = range(0,12))


tvector = np.array(Tdata[1:,4:11],dtype = float)#accepted truth


Pvector = tvector*0
Bvector = tvector*0
Worst = tvector*0
Worst[:,0] = 1

i = 0
for r in Tdata[1:]:
    fname = r[0]
    surname = r[1]
    zipcode = r[2]
    
    Probs,bad_Probs = BISFG_func(fname,surname,zipcode,plot = False)
    for race in Races:
        Pvector[i,Races[race]] = Probs[race]
        Bvector[i,Races[race]] = bad_Probs[race]
    i+=1

import matplotlib.pyplot as plt
import matplotlib.colors
#import seaborn as sns

races = ['White','Black','API','AIAN','Multi','Hisp','Other']

N = 256
vals = np.ones((N, 4))
vals[:, 0] = np.linspace(90/256, 1, N)*0
vals[:, 1] = np.linspace(90/256, 1, N)*0
vals[:, 2] = np.linspace(90/256, 1, N)
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

    
    

def confusion(T, P):
    t = np.argmax(T, axis=1)
    p = np.argmax(P, axis=1)

    # Plot for each race
    fig, axs = plt.subplots(1, 7, figsize=(20, 10))  # Adjust the layout as needed
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

        c = np.array([[TP, FN], [FP, TN]])

        confusion_plot(c,['True','False'],axs[x])
        axs[x].set_title(r)
    
    
    
    plt.tight_layout()
    
    multiclass = np.zeros((7,7),dtype = int)
    
    indices = np.column_stack((t,p))
    print(indices)
    for i in indices:
        multiclass[i[0],i[1]] += 1
    
    fig, axs = plt.subplots(1, 1, figsize=(20, 10))
    #axs = axs.flatten()
    confusion_plot(multiclass,races,axs)
    plt.title('Multi-class Confusion Matrix')
    
    plt.show()



    
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

C = confusion(Pvector,tvector)

print(C)