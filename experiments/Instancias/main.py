from pathlib import Path
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import time
from instanceGeneratorGeneral import generarInstancias 

metodos = ["FB", "BT-F", "BT-O", "BT", "DP"]
columnas = ['Tiempo de ejecución (10^(-3) s)', 'Algoritmo ', 'Cantidad de locales', 'Res', 'Familia', 'contagios']

familias = ['familias/peorCaso','familias/mejorCaso','familias/casoReal', 'familias/ordenadoPorBeneficioDescendente', 'familias/ordenadoPorBeneficioAscendente','familias/casoRandom' ,'familias/contagios']

def leer_instancia(path_instancia):
    with open(path_instancia, "r") as f:
        return f.read()


def correr_experimento(metodo, familia, locales, iteraciones, instanciasDistintas, contagio = 0): ### Recibe un  metodo, una instancia .txt y la cantidad de iteraciones y devuelve el promedio del tiempo de ejecucion y el resultado
    
    tiempos_de_ejecucion = []
    
    for j in range(0, instanciasDistintas):
        #print(str(instancia_path))
        instancia_path = generarInstancias(familia,locales,contagio)
        instancia = leer_instancia(str(instancia_path))
        #print(instancia)
        for i in range(0,iteraciones):
        # Crear proceso para ejecutar el codigo.
                process = subprocess.Popen(["../../main", metodo], stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines = True)
                #print(metodo , instancia)

                process.stdin.write(instancia)
            
        # Poner la instancia en la entrada estandar.
                process.stdin.flush()

        # Correr experimento.
                exit_code = process.wait()
            
        # Verificar que el proceso no fallo.
                if exit_code != 0: raise(F"Hubo un error en la experimentacion para el algoritmo: " + metodo + " con la instancia " + instancia )

        # Leer salida de STDERR con los tiempos de ejecucion de cada metodo.
                #print(((process.stderr.read())))
                
                tiempos_de_ejecucion.append(float(process.stderr.read()))
                res = float(process.stdout.read())

                process.stdin.close()
                process.stdout.close()
                process.stderr.close()
    #print(tiempos_de_ejecucion)

    mean = np.mean(tiempos_de_ejecucion, axis=0)
    sd = np.std(tiempos_de_ejecucion, axis=0)
    #print(len(tiempos_de_ejecucion))
    final_list = [x for x in tiempos_de_ejecucion if (x > mean - 2 * sd)]
    final_list = [x for x in final_list if (x < mean + 2 * sd)]
    #print(len(final_list))
    return(np.mean(final_list), res)


def correlacion_pearson(data_frame, columna1, columna2):
    return np.corrcoef(data_frame[columna1], data_frame[columna2])[0,1]

def experimentoFB(iteraciones, instanciasDistintas, cantidadLocales):
    print('EXPERIMENTO FUERZA BRUTA')
    listaDeFrames = []
    for fam in tqdm(familias[:-1]):
        for locales in range(1, cantidadLocales+1):
           # print(str(fam) +'/'+ entry.name)
            tiempo, res = correr_experimento(metodos[0], fam[9:], locales, iteraciones, instanciasDistintas) ## Devuelve el promedio de un tiempo de ejecucion       
            values =  {columnas[0]: [tiempo], columnas[1] : metodos[0], columnas[2]: locales, columnas[3]: res, 'tiempoEsperado': [], columnas[4]: fam[9:] }
            df = pd.DataFrame(data = values, columns=columnas)
            listaDeFrames.append(df)

    fd = pd.concat([listaDeFrames[i] for i in range(len(listaDeFrames))], ignore_index=True)
    # Graficamos los tiempos de ejecución de cada dataset en función de n.
    
    
    # Calculamos los tiempos de ejecución de acuerdo a la cantidad de tiendas.

    fd["tiempoEsperado"] = 2.0 ** fd[columnas[2]] * (0.000015 / 2.5); # Exponencial
  
    fig = plt.figure()
    
    ax1 = sns.scatterplot(data=fd, x=columnas[2], y=columnas[0], hue=columnas[4],legend = "brief").set_title("Tiempos de ejecución de FB experimentales vs teórico")
    ax2 = sns.lineplot(data=fd, x=columnas[2], y='tiempoEsperado', color="orange", legend = True , label = 'O(2^n)')
    plt.legend(title=False)
    
    
    #legends.insert(1, 'xd')
    # Leyenda con el tiempo experimental de cada familia y el tiempo teórico

    plt.savefig("./fb-Complejidad.svg",bbox_inches="tight")
    plt.clf()
    #Creamos la categoría Complejidad.
    fd["Complejidad - O(2^n)"] = 2.0 ** fd[columnas[2]]
    
    #Creamos un lineplot entre la Complejidad(O (2^n)) y el tiempo esperado. Hace una linea correcta porque hay correlación.
    fig = sns.lmplot(data=fd, x=columnas[0], y="Complejidad - O(2^n)", hue = columnas[4], legend= False)
    plt.title("Correlación de tiempo de ejecución con complejidad esperada")
    plt.legend(loc = 'upper left', title = 'Familia')
    print(fd.to_markdown())
    plt.savefig("./fb-correlacion.svg",bbox_inches="tight")
    plt.clf()
    print("Índice de correlación de Pearson:", correlacion_pearson(fd, columnas[0], "Complejidad - O(2^n)"))


def experimentoPeorCaso(iteraciones, instanciasDistintas, cantidadLocales): #Recibe la cantidad de iteraciones, hace un grafico.
    print('EXPERIMENTO PEOR CASO')
    listaDeFrames = []
    fam = familias[0] #CASO PEOR
    metodosBT = metodos[1:-1]
    for locales in tqdm(range(1, cantidadLocales+1)):
        if locales > 31:
            metodosBT = ["BT", "BT-F"]
        
        
        for metodo in metodosBT:
            tiempo, res = correr_experimento(metodo, fam[9:], locales, iteraciones, instanciasDistintas) ## Devuelve el promedio de un tiempo de ejecucion       
            values =  {columnas[0]: [tiempo], columnas[1] : metodo, columnas[2]: locales, columnas[3]: res, 'tiempoEsperado': [], columnas[4]: fam[9:] }
            df = pd.DataFrame(data = values, columns=columnas)
            listaDeFrames.append(df)

    fd = pd.concat([listaDeFrames[i] for i in range(len(listaDeFrames))], ignore_index=True)
    
    fig3 = sns.scatterplot(data=fd, x=columnas[2], y=columnas[0], hue=columnas[1],legend = "brief").set_title("Tiempos de ejecución de algoritmos de Backtracking en peor caso")
    plt.savefig('PeorCaso.svg',bbox_inches="tight")
    plt.clf()

    
    fd["Complejidad - O(2^n)"] = 2.0 ** fd[columnas[2]];
    fig = sns.lmplot(data=fd, x=columnas[0], y="Complejidad - O(2^n)", hue = columnas[1], legend= False)
    plt.title("Correlación de tiempo de ejecución con complejidad esperada")
    plt.legend(loc = 'upper left',title = 'Algoritmo')
    print(fd.to_markdown())
    plt.savefig("./PeorCaso-correlacion.svg",bbox_inches="tight")
    plt.clf()
    
    print("Índice de correlación de Pearson de " + metodos[1] + " :", correlacion_pearson(fd[fd[columnas[1]]==metodos[1]], columnas[0], "Complejidad - O(2^n)"))
    print("Índice de correlación de Pearson de " + metodos[2] + " :", correlacion_pearson(fd[fd[columnas[1]]==metodos[2]], columnas[0], "Complejidad - O(2^n)"))
    print("Índice de correlación de Pearson de " + metodos[3] + " :", correlacion_pearson(fd[fd[columnas[1]]==metodos[3]], columnas[0], "Complejidad - O(2^n)"))

def experimentoMejorCaso(iteraciones, instanciasDistintas, cantidadLocales): #Recibe la cantidad de iteraciones, hace un grafico.
    print('EXPERIMENTO MEJOR CASO')
    listaDeFrames = []
    fam = familias[1] #MEJOR CASO
    metodosBT = metodos[1:-1]
    for locales in tqdm(range(1, cantidadLocales+1)):
        tiemposPorMetodo = []
        for metodo in metodosBT:
            
            tiempo, res = correr_experimento(metodo, fam[9:], locales, iteraciones, instanciasDistintas) ## Devuelve el promedio de un tiempo de ejecucion  
            tiemposPorMetodo.append(tiempo)  
   
        values =  {columnas[0]: tiemposPorMetodo, columnas[1] : metodosBT, columnas[2]: locales, columnas[3]: res, 'tiempoEsperado': [], columnas[4]: fam[9:] }
        df = pd.DataFrame(data = values, columns=columnas)
        listaDeFrames.append(df)


    fd = pd.concat([listaDeFrames[i] for i in range(len(listaDeFrames))], ignore_index=True)
    
    fig3 = sns.relplot(data=fd, x=columnas[2], y=columnas[0], hue=columnas[1], kind = "line",legend = "brief")
    plt.title("Tiempos de ejecución de algoritmos de Backtracking en mejor caso")
    
    plt.savefig('MejorCaso.svg',bbox_inches="tight")
    plt.clf()

    
    fd["Complejidad - O(n)"] = fd[columnas[2]];
    fig = sns.lmplot(data=fd, x=columnas[0], y="Complejidad - O(n)", hue = columnas[1], legend= False)
    plt.legend(loc = 'upper left', title = 'Algoritmo')
    plt.title("Correlación de tiempo de ejecución con complejidad esperada")
    print(fd.to_markdown())
    plt.savefig("./MejorCaso-correlacion.svg",bbox_inches="tight")
    plt.clf()
    print("Índice de correlación de Pearson de " + metodos[1] + " :", correlacion_pearson(fd[fd[columnas[1]]==metodos[1]], columnas[0], "Complejidad - O(n)"))
    print("Índice de correlación de Pearson de " + metodos[2] + " :", correlacion_pearson(fd[fd[columnas[1]]==metodos[2]], columnas[0], "Complejidad - O(n)"))
    print("Índice de correlación de Pearson de " + metodos[3] + " :", correlacion_pearson(fd[fd[columnas[1]]==metodos[3]], columnas[0], "Complejidad - O(n)"))


def experimentoCasoRandom(iteraciones, instanciasDistintas, cantidadLocales): 
    """Recibe la cantidad de iteraciones, hace un grafico."""
    print('EXPERIMENTO CASO RANDOM')
    listaDeFrames = []
    fams = familias[3:6] #CASO RANDOM
    metodo = "BT"
    #metodosBT = ["BT", "BT-F", "BT-O"]
    #for metodo in metodosBT:
    for fam in fams:
        for locales in tqdm(range(1, cantidadLocales+1)):
            tiemposPorMetodo = []
            tiempo, res = correr_experimento(metodo, fam[9:], locales, iteraciones, instanciasDistintas) ## Devuelve el promedio de un tiempo de ejecucion  
            tiemposPorMetodo.append(tiempo)  
    
            values =  {columnas[0]: tiemposPorMetodo, columnas[1] : metodo, columnas[2]: locales, columnas[3]: res, 'tiempoEsperado': [], columnas[4]: fam[9:] }
            df = pd.DataFrame(data = values, columns=columnas)
            listaDeFrames.append(df)

    fd = pd.concat([listaDeFrames[i] for i in range(len(listaDeFrames))], ignore_index=True)
    
    fig3 = sns.scatterplot(data=fd, x=columnas[2], y=columnas[0], hue=columnas[4],style = columnas[1],legend = "brief").set_title("Tiempos de ejecución de algoritmos de Backtracking de acuerdo al orden")
    
    plt.savefig('CasoRandom.svg',bbox_inches="tight")
    plt.clf()

    

def heatmapDP(iteraciones, instanciasDistintas, cantidadLocales):
    print("Haciendo heatmap de dp")
    listaDeFrames = []
    contagios = [i for i in range(1000, 8500, 500)]
    locales = [i for i in range(1000, 8500, 500)]
    columnasDP = ["Contagio", "Cantidad de locales", "Tiempo de ejecución (10^-3)s"]
    fam = familias[-1]
    for local in tqdm(locales):
        for contagio in contagios:
            tiempo, res = correr_experimento("DP", fam[9:], local, iteraciones, instanciasDistintas, contagio) ## Devuelve el promedio de un tiempo de ejecucion  
            values = { columnasDP[0] : [contagio] , columnasDP[1] : [local], columnasDP[2]: [tiempo]}
            df = pd.DataFrame(data = values, columns=columnasDP)
            listaDeFrames.append(df)

    fd = pd.concat([listaDeFrames[i] for i in range(len(listaDeFrames))], ignore_index=True)
    print(fd.to_markdown())
    df_heatmap = fd.pivot(index=columnasDP[0], columns=columnasDP[1], values=columnasDP[2])
    print(df_heatmap.to_markdown())
    fig = sns.heatmap(df_heatmap, cmap= sns.cm.rocket, cbar_kws={'label': 'Tiempos de ejecución (10^-3)s'});
    fig.invert_yaxis();
    plt.title("Tiempo de ejecución en función de contagio máximo y cantidad de locales")
    plt.savefig("dp-heatmap.svg",bbox_inches="tight");
    listaDeFrames = []
    


def experimentoDP(iteraciones, instanciasDistintas, cantidadLocales):
    """Recibe la cantidad de iteraciones, hace un grafico."""
    print('EXPERIMENTO DP VS BT')
    listaDeFrames = []
    contagios = [100, 200, 300]
    fam = familias[6] #CASO CONTAGIOS VARIABLES
    metodosBTvsDP = metodos[-2:]
    
    for locales in tqdm(range(1, cantidadLocales+1)):
        for contagio in (contagios):
            tiemposPorMetodo = []
            for metodo in metodosBTvsDP:
                #print(metodo)
                tiempo, res = correr_experimento(metodo, fam[9:], locales, iteraciones, instanciasDistintas, contagio) ## Devuelve el promedio de un tiempo de ejecucion  
                tiemposPorMetodo.append(tiempo)  
    
            values =  {columnas[0]: tiemposPorMetodo, columnas[1] : metodosBTvsDP, columnas[2]: locales, columnas[3]: res, 'tiempoEsperado': [], columnas[4]: fam[9:], 'contagios' : contagio }
            df = pd.DataFrame(data = values, columns=columnas)
            listaDeFrames.append(df)

    fd = pd.concat([listaDeFrames[i] for i in range(len(listaDeFrames))], ignore_index=True)
    print(fd.to_markdown())
    pal = sns.color_palette("light:#5A9", as_cmap=True)
    fig3 = sns.scatterplot(data=fd, x=columnas[2],y=columnas[0],hue='contagios',legend = "full", style = columnas[1]).set_title("Tiempos de ejecución de algoritmos BT vs DP")
    
    plt.savefig('BTvsDPPRUEBA.svg',bbox_inches="tight")
    plt.clf()


#experimentoPeorCaso(10,1,45)
#experimentoFB(10,10,25)
#experimentoMejorCaso(100,1,100)
#experimentoCasoRandom(10,20,25)
#experimentoDP(10,10,30)
heatmapDP(10, 1,0)
