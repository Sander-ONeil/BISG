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
    
print(Pvector)
i = 0
total = np.array([57.83619335,12.05021108,6.10673734,0.67934949,4.08779979,18.72987741,.01])
races = ['White','Black','API','AIAN','Multi','Hisp','Other']
X = np.zeros((8,500))
Y = np.zeros((8,500))

i = 0


t = np.argmax(tvector,axis=1)
for x in range(-100,100):
    x = x/100
    

    Pvector2 = Pvector / ((total)**x)
    
    P = np.argmax(Pvector2, axis=1)
    #print(P)
    print(np.sum((P == t)), 'out of ', np.sum((P == t)==False) + np.sum((P == t)))
    
    p = np.argmax(Pvector2, axis=1)
    
    for x1, r in enumerate(races):
        pp = p == x1
        pn = pp == False
        tp = t == x1
        tn = tp == False

        TP = np.sum(pp & tp)
        FP = np.sum(pp & tn)
        TN = np.sum(pn & tn)
        FN = np.sum(pn & tp)
        print(x1,i,' ****************************')
        Y[x1,i] = TP /(TP+FN)
        X[x1,i] = FP/ (FP+TN)
    i+=1
print(X)
import matplotlib.pyplot as plt

# plt.plot(np.swapaxes(X[:,:],0,1),np.swapaxes(Y[:,:],0,1))
# plt.xlabel('TP / P')
# plt.ylabel('FP/ p')
# plt.legend(races)
# plt.title('Dividing by significance (Total US racial breakdown)')
# plt.show()

    
# Plot for each race
fig, axs = plt.subplots(4, 2, figsize=(10, 20))  # Adjust the layout as needed
axs = axs.flatten()

for x, r in enumerate(races):
    
    axs[x].set_xlabel('TP / P')
    axs[x].set_ylabel('FP/ p')
    axs[x].plot(X[x],Y[x])
    axs[x].set_title(r)
plt.show()