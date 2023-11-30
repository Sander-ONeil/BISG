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

races = ['White','Black','API','AIAN','Multi','Hisp','Other']

def confusion(T,P):
    t = np.argmax(T,axis = 1)
    p = np.argmax(P,axis = 1)
    c = np.zeros((2,2),dtype = int)
    
    
    
    for x,r in enumerate(races):
        pp = p == x
        pn = pp == False
        tp = t == x
        tn = tp == False
        
        TP = pp & tp
        FP = pp & tn
        TN = pn & tn
        FN = pn & tp
        
        c[0] = [np.sum(TP),np.sum(FN)]
        c[1] = [np.sum(FP),np.sum(TN)]
        print(g_mas_order[x])
        print(c)
    
    multiclass = np.zeros((7,7),dtype = int)
    
    indices = np.column_stack((t,p))
    print(indices)
    for i in indices:
        multiclass[i[0],i[1]] += 1
    
    print(multiclass)
    
    return c


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