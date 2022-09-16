import random
import numpy as np
import os

tuplas = []

def generateOrdenadasPorBeneficio(cantTiendas, reverse):
    OrdenadasPorBeneficio = sorted(tuplas, key= lambda x: x[0], reverse=reverse)
    contLimit = 1000
    beneficioGeneration =  str(cantTiendas)+" "+str(contLimit)+ " "
    P = 2 * contLimit / cantTiendas
    it = int(cantTiendas)
    for i in range(0, it):
        beneficioGeneration+= str(OrdenadasPorBeneficio[i][0]) + " "+ str(OrdenadasPorBeneficio[i][1]) + " "

    directory = "ordenadoPorBeneficio"

    parent_dir = "../familias/"

    path = os.path.join(parent_dir, directory)
    try: 
        os.mkdir(path) 
    except OSError as error: 
       print("")

    f = open(parent_dir + directory +"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(beneficioGeneration + " ")
    f.close()


def generateOrdenadasPorContagio(cantTiendas):
    OrdenadasPorContagio = sorted(tuplas, key= lambda x: x[1], reverse=False)
    contLimit = 1000
    beneficioGeneration =  str(cantTiendas)+" "+str(contLimit)+ " "
    P = 2 * contLimit / cantTiendas
    it = int(cantTiendas)
    for i in range(0, it):
        beneficioGeneration+= str(OrdenadasPorContagio[i][0]) + " "+ str(OrdenadasPorContagio[i][1]) + " "

    directory = "ordenadoPorContagio"

    parent_dir = "../familias/"

    path = os.path.join(parent_dir, directory)
    try: 
        os.mkdir(path) 
    except OSError as error: 
       print("")

    f = open(parent_dir + directory +"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(beneficioGeneration + " ")
    f.close()

    
# cantTiendas = input("cuantas tiendas generar?")
def generate(cantTiendas):
    contLimit = 1000
    casoRealGeneration =  str(cantTiendas)+" "+str(contLimit)+ " "
    P = 2 * contLimit / cantTiendas
    
    it = int(cantTiendas)
    for i in range(0, it):
        beneficio = 10* int(np.random.chisquare(10))
        contagio = np.random.random_integers(0.90*P, 1.1 * P)
        tuplas.append((beneficio,contagio)) 
        casoRealGeneration+= str(beneficio) + " "+ str(contagio) + " "
        
        
    directory = "casoReal"
      
    parent_dir = "../familias/"

    path = os.path.join(parent_dir, directory)
    try: 
        os.mkdir(path) 
    except OSError as error: 
       pass

    f = open(parent_dir + directory +"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(casoRealGeneration+ " ")
    f.close()
    generateOrdenadasPorBeneficio(cantTiendas, True)
    generateOrdenadasPorBeneficio(cantTiendas, False)
    
    #generateOrdenadasPorContagio(cantTiendas)
    return parent_dir + directory +"/C"+str(cantTiendas)+ ".txt"
