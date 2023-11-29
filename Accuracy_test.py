from BIFSG import *

Probs,bad_Probs = BISFG_func(fname,surname,zipcode,plot = False)
g_mas_order = ['White','Black','API','AIAN','Multi','Hisp','Other']
Races = {"2 Races":4,"Alaskan/American Native":3,"Asian/Pacific Islander":2,"Black":1,"Hispanic":5,"White":0,"Other":6}
        

Tdata = np.loadtxt( os.path.dirname(os.path.abspath(__file__))+'/'+'Truth_data.csv',
                 delimiter=",", dtype=str,usecols = range(0,12))


print(Tdata[:,:])

tvector = np.array(Tdata[1:,4:11],dtype = float)#accepted truth

print(tvector)

Pvector = tvector*0
Bvector = tvector*0

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
        
print(np.linalg.norm(Pvector-tvector,axis = 1))
print(np.linalg.norm(Bvector-tvector,axis = 1))