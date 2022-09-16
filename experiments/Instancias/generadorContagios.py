import random
import numpy as np
import os

def generate(cantTiendas, contLimit):
    tuplas = []
    P = 2 * contLimit / cantTiendas
    casoRealGeneration = str(cantTiendas)+ " " + str(contLimit)+ " "
    it = int(cantTiendas)
    for i in range(1, it+1):
        #beneficio = random.randint(1,1+it*4)
        #contagio = random.randint(1, contLimit)
        beneficio = 10* int(np.random.chisquare(10))
        contagio = np.random.random_integers(0.90*P, 1.1 * P)
        tuplas.append((beneficio,contagio)) 
        casoRealGeneration+= str(beneficio) + " " + str(contagio) + " "
        
        
    directory = "contagio" + str(contLimit) 

    parent_dir = "../familias/contagios"

    path = os.path.join(parent_dir, directory)
   
    try: 
        os.mkdir(path)
    except OSError as error: 
        pass

    f = open(str(path) +"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(casoRealGeneration+ " ")
    f.close()
    return str(path) +"/C"+str(cantTiendas)+ ".txt"
    




    
