import random
import os
# cantTiendas = input("cuantas tiendas generar?")
def generate(cantTiendas):
    contLimit = random.randint(1, random.randint(1,cantTiendas * 10))
    randomNumberGeneration=""
    maxOut=0
    numberList = []
    it = int(cantTiendas)*2 - 2 
    for i in range(0, it):
        if (i % 2) == 0 :
            rn = random.randint(1,100)
            maxOut = maxOut if maxOut > rn else rn
            randomNumberGeneration+=" "+str(rn) 
        else:
            rn = random.randint(1, contLimit)  
            randomNumberGeneration+=" "+str(rn)

    randomNumberGeneration = str(cantTiendas)+" "+str(contLimit)+ randomNumberGeneration  +" "+ str(maxOut + random.randint(0,5)) +" "+ str(random.randint(1, contLimit)) + " "
    
    directory = "testInstancesBiggerLast"
      
    parent_dir = "../familias/"

    path = os.path.join(parent_dir, directory)
    try: 
        os.mkdir(path) 
    except OSError as error:
    	pass

    f = open(parent_dir + directory+"/C"+str(cantTiendas)+ ".txt", "w", encoding="utf-8")
    f.write(randomNumberGeneration)
    f.close()

