import random
import os
# cantTiendas = input("cuantas tiendas generar?")
def generate(cantTiendas):
    contLimit = 1
    peorCasoGeneration= str(cantTiendas) + " " + str(contLimit) + " "
    it = int(cantTiendas) 
    for i in range(0, it-1):
        beneficio = 0
        #beneficio = i**2
        contagio = 0
        peorCasoGeneration+= str(beneficio) + " " + str(contagio) + " "
        
    contagioExtremo = 2
    beneficioExtremo = int(10e6)
    peorCasoGeneration+= str(beneficioExtremo) + " " + str(contagioExtremo)
    
    directory = "peorCaso"
      
    parent_dir = "../familias/"

    path = os.path.join(parent_dir, directory)
    try: 
        os.mkdir(path) 
    except OSError as error:
    	pass

    f = open(parent_dir + directory+"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(peorCasoGeneration + " ")
    f.close()
    return parent_dir + directory+"/C"+str(cantTiendas)+ ".txt"
