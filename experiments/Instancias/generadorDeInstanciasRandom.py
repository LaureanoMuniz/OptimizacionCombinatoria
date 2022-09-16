import random
import os

# cantTiendas = input("cuantas tiendas generar?")
def generate(cantTiendas):
    contLimit = random.randint(1,cantTiendas * 2)
    randomNumberGeneration =  str(cantTiendas)+" "+str(contLimit) + " "
    it = int(cantTiendas)*2 
    for i in range(0, it+1):
        rn=0
        if (i % 2) == 0 :
            rn = random.randint(1,1+it*4)
        else:
            rn = random.randint(1, contLimit)  
        randomNumberGeneration+=" "+str(rn)
    directory = "testInstancesRandom"
      
    parent_dir = "../familias/"

    path = os.path.join(parent_dir, directory)
    try: 
        os.mkdir(path) 
    except OSError as error: 
       pass

    f = open(parent_dir + directory +"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(randomNumberGeneration+ " ")
    f.close()
    return parent_dir + directory +"/C"+str(cantTiendas)+ ".txt"

def tuplasRandom(cantTiendas, contLimit) :
    tuplas = []
    for i in range(0, cantTiendas+1):
        beneficio = random.randint(1,1+i*4)
        contagio = random.randint(1, contLimit) 
        tuplas.append((beneficio,contagio)) 
    return tuplas

def generateDescending(cantTiendas):  
    contLimit = random.randint(1,cantTiendas * 2) # Modifique esto porque se rompia en un caso
    randomNumberGeneration =  str(cantTiendas)+" "+str(contLimit) + " "
    tuplas = sorted(tuplasRandom(cantTiendas, contLimit), key= lambda x: x[0], reverse=True)
    for i in range(0, cantTiendas):
        randomNumberGeneration+= str(tuplas[i][0]) + " "+ str(tuplas[i][1]) + " "
    
    directory = "testInstancesRandomDescending"
    parent_dir = "../familias/"
    path = os.path.join(parent_dir, directory)
    try: 
        os.mkdir(path) 
    except OSError as error: 
       pass

    f = open(parent_dir + directory +"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(randomNumberGeneration+ " ")
    f.close()
    return parent_dir + directory +"/C"+str(cantTiendas)+ ".txt"

def generateAscending(cantTiendas):
    contLimit = random.randint(1,cantTiendas * 2) #Modifique esto porque se rompia en un caso
    randomNumberGeneration =  str(cantTiendas)+" "+str(contLimit) + " "
    tuplas = sorted(tuplasRandom(cantTiendas, contLimit), key= lambda x: x[0], reverse=False)
    for i in range(0, cantTiendas):
        randomNumberGeneration+= str(tuplas[i][0]) + " "+ str(tuplas[i][1]) + " "
        
    directory = "testInstancesRandomAscending"
    parent_dir = "../familias/"
    path = os.path.join(parent_dir, directory)
    try: 
        os.mkdir(path) 
    except OSError as error: 
       pass

    f = open(parent_dir + directory +"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(randomNumberGeneration+ " ")
    f.close()
    return parent_dir + directory +"/C"+str(cantTiendas)+ ".txt"
