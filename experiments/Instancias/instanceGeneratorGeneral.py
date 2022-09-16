
import random
import os
import shutil
from generadorDeCasosReales import generate as realesGen
from generadorDePeorCaso import generate as peorGen
from generadorDeMejorCaso import generate as mejorGen
from generadorContagios import generate as contagiosGen
from generadorDeInstanciasRandom import generateDescending as randomGenDescending
from generadorDeInstanciasRandom import generateAscending as randomGenAscending
from generadorDeInstanciasRandom import generate as randomGen

parent_dir = "../familias/" 
dir = parent_dir + "contagios"
try: 
    shutil.rmtree(parent_dir)
    shutil.rmtree(dir)
    os.mkdir(parent_dir)
    os.mkdir(dir)
except OSError as error: 
    os.mkdir(parent_dir)
    os.mkdir(dir)

instancesList = [i for i in range(1,31)]

#for instance in instancesList:
#     realesGen(instance)
#     peorGen(instance)
    
#     contagiosGen(instance)    

# for i in range(1,100):
#     mejorGen(i)


def generarInstancias(instanceType,n, contagio = 0):
    if(instanceType=="peorCaso") :
        return peorGen(n)
    elif(instanceType=="mejorCaso") :
        return mejorGen(n)
    elif(instanceType=="casoReal") :
        return realesGen(n)
    elif(instanceType=="casoRandom") :
        return randomGen(n)
    elif(instanceType=="ordenadoPorBeneficioDescendente") :
        return randomGenDescending(n)
    elif(instanceType=="ordenadoPorBeneficioAscendente") :
        return randomGenAscending(n)
    elif(instanceType=="contagios") :
        return contagiosGen(n, contagio)


