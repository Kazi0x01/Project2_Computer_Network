import pickle
from random import randint, random
from Event_class import highLevelMessage 

HEADERSIZE = 10

my_objects = []
my_objects.append(highLevelMessage("crash","1:04pm",53.199451902831555,-6.976318359375001))
my_objects.append(highLevelMessage("ambulance","2:45pm",54.199451902831555,-7.976318359375001))
my_objects.append(highLevelMessage("slippery roads","3:07pm",52.199451902831555,-9.976318359375001))
my_objects.append(highLevelMessage("crash","3:25pm",52.199451902831555,-8.976318359375001))




def get_event():
    leng = len(my_objects)
    idx = randint(0, leng-1)
    obj1 = my_objects[idx]
    n_data = pickle.dumps(obj1)
    n_data = bytes("{}".format(len(n_data) < HEADERSIZE).encode('utf-8'))+n_data
    
    return n_data




