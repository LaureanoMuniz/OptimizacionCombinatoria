import random
import os

# cantTiendas = input("cuantas tiendas generar?")
def generate(cantTiendas):
    contLimit = 1
    peorCasoGeneration= str(cantTiendas) + " " + str(contLimit) + " "
    it = int(cantTiendas) 
    for i in range(0, it):
        beneficio = 0
        #beneficio = i**2
        contagio = 2
        peorCasoGeneration+= str(beneficio) + " " + str(contagio) + " "
        
    
    directory = "mejorCaso"
      
    parent_dir = "../familias/"

    path = os.path.join(parent_dir, directory)
    try: 
        os.mkdir(path) 
    except OSError as error:
    	pass

    f = open(parent_dir + directory+"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(peorCasoGeneration+ " ")
    f.close()
    return parent_dir + directory+"/C"+str(cantTiendas)+ ".txt"
