Para correr la experimentación:

1. Correr en consola "sudo pip3 install -r requirements.txt"
2. Hacer un make en este directorio para compilar main.cpp
3. Ir al directorio ./experiments/Instancias/
4. Comentar al final de main.py los experimentos que se desean correr. Pueden cambiarse la cantidad de repeticiones y de instancias generadas.
5. Correr main.py

Nótese que los graficos se generan en el directorio ./experiments/Instancias. En ./experiments/Instancias/graficos se encuentran los graficos del informe.


Para correr un caso particular:

1. Hacer un make en este directorio para compilar main.cpp
2. Llamar main.cpp con alguno de los siguientes parametros

"FB": Para resolver con brute force
"BT-F": Para resolver con Backtracking con poda de factibilidad
"BT-O": Para resolver con Backtracking con poda de optimización
"BT": Para resolver con Backtracking con mezcla de ambas podas.
"DP": Para resolver con Programación dinamica.

3. Introducir luego la instancia que se quiere resolver con formato

n cantidad de locales de la avenida
M limite de contagio
(bi, ci) beneficio y contagio del local i

Ejemplo

./main DP 
5 45
50 10
25 10
10 20
20 30
15 20

OUTPUT: Tiempo de ejecución y maximo beneficio que se puede conseguir.
# OptimizacionCombinatoria
