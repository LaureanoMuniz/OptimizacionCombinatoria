#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <chrono>
#include <set>
#include <map>
#include <tuple>
using namespace std;
int maximo = 0;
int contagioLimite, cantTiendas;
vector<tuple<int, int>> tiendas;

int iteraciones = 0;
int FB(int tienda, bool noHayContiguos, int cont_parcial, int ben_parcial,  bool ultimo){
    if(tienda == cantTiendas){ //caso Base
        if(noHayContiguos && cont_parcial <= contagioLimite){ //es Factible?
            return ben_parcial;
        }
        return 0;
    }else{
        return max(
            FB(tienda+1,  ultimo ? false : noHayContiguos , cont_parcial + get<1>(tiendas[tienda]), ben_parcial + get<0>(tiendas[tienda]), true),
            FB(tienda+1, noHayContiguos, cont_parcial, ben_parcial, false)
        );
    }
}



int BTF(int tienda, bool ultimo, int cont_parcial, int ben_parcial){
    
    if(tienda == cantTiendas){
        return ben_parcial;
    }else{
        int hijoDerecho=0;
        int hijoIzquierdo=0;
        if(!ultimo && cont_parcial + get<1>(tiendas[tienda]) <= contagioLimite){
            hijoIzquierdo=BTF(tienda + 1, true, cont_parcial + get<1>(tiendas[tienda]), ben_parcial + get<0>(tiendas[tienda]));
        }
        hijoDerecho=BTF(tienda + 1 , false, cont_parcial, ben_parcial);
        //cout << hijoIzquierdo << ' ' <<hijoDerecho<< ' '<<  tienda<< endl;
        return max(hijoIzquierdo, hijoDerecho);
    }
}


int BTO(int tienda, int noHayContiguos, int cont_parcial, int ben_parcial, bool ultimo ,int sumaRestante){
   
    if(tienda == cantTiendas){
        if(noHayContiguos && cont_parcial <= contagioLimite){
            maximo = maximo < ben_parcial ? ben_parcial : maximo;
        }
        return maximo;
    }else{
        int hijoDerecho=0;
        int hijoIzquierdo=0;
        if( sumaRestante + ben_parcial > maximo){ //Cota de Optimalidad, La suma actual más lo que falta por sumar supera el máximo actual?
            hijoIzquierdo = BTO( tienda+1,  ultimo ? false : noHayContiguos , cont_parcial + get<1>(tiendas[tienda]), ben_parcial + get<0>(tiendas[tienda]), true, sumaRestante - get<0>(tiendas[tienda]));
            if(sumaRestante + ben_parcial > maximo){ //Puede haber cambiado el máximo y ahorrarnos llamados recursivos
                hijoDerecho = BTO(tienda+1, noHayContiguos, cont_parcial, ben_parcial , false, sumaRestante - get<0>(tiendas[tienda]));
            }
            return max(hijoIzquierdo, hijoDerecho);
        }
        return 0;
    }
}

int BT(int tienda, int cont_parcial, int ben_parcial, bool ultimo, int sumaRestante){
    
    if(tienda == cantTiendas){
        if(maximo < ben_parcial) maximo = ben_parcial;
        return maximo;
    }else{
        int hijoDerecho = 0;
        int hijoIzquierdo = 0;
        if((ben_parcial+ sumaRestante) > maximo){ //poda de optimalidad
            if(ultimo == false && cont_parcial + get<1>(tiendas[tienda]) <= contagioLimite){ //poda Factibilidad
                hijoIzquierdo = BT(tienda+1, cont_parcial + get<1>(tiendas[tienda]), ben_parcial + get<0>(tiendas[tienda]), true,  sumaRestante - get<0>(tiendas[tienda])); //sumar la tienda
            }
            if((ben_parcial + sumaRestante) > maximo) //el máximo puede cambiar asi que volvemos a preguntar la guarda;
                hijoDerecho = BT(tienda+1, cont_parcial, ben_parcial, false, sumaRestante - get<0>(tiendas[tienda]));

            return max(hijoIzquierdo, hijoDerecho);
        }
        return 0;
    }
}

int PD(int i, int c, vector<vector<int>> & M ){ // Maximo beneficio que podemos obtener seleccionando un subconjunto con los
                                                            // locales i,i+1,...,n con contagio c

    if(i > cantTiendas || i < 0) return 0;
    if(c > contagioLimite || c < 0) return 0;
    if (M[i][c] == -1){ // Si aun no esta definido
        if ( i == cantTiendas){ //   Si el subconjunto tiene 0 locales
            M[i][c] = 0;
            
        }
        if ( get<1>(tiendas[i]) > c){
            M[i][c] = PD(i+1, c, M);
            


        }else{
            
            M[i][c] = max(get<0>(tiendas[i]) + PD(i+2,c - get<1>(tiendas[i]), M ), PD(i+1, c, M)); // Maximo habiendome agregado a mi y no habiendome agregado. Si me agregue a mi tengo que preguntar dos mas arriba.
        }
    }

	return M[i][c];
}

int main(int argc, char **argv){
	// Leemos el parametro que indica el algoritmo a ejecutar.
	map<string, string> algoritmos_implementados = {
		{"FB", "Fuerza Bruta"},
        {"BT", "Backtracking con podas"},
        {"BT-F", "Backtracking con poda por factibilidad"},
        {"BT-O", "Backtracking con poda por optimalidad"},
        {"DP", "Programacion dinámica"}
    };

	// Verificar que el algoritmo pedido exista.
	if (argc < 2 || algoritmos_implementados.find(argv[1]) == algoritmos_implementados.end()){
		cerr << "Algoritmo no encontrado: " << argv[1] << endl;
		cerr << "Los algoritmos existentes son: " << endl;
		for (auto &alg_desc : algoritmos_implementados)
			cerr << "\t- " << alg_desc.first << ": " << alg_desc.second << endl;
		return 0;
	}
	string algoritmo = argv[1];
	// Leemos el input.
	cin >> cantTiendas >> contagioLimite;
	for (int i = 0; i < cantTiendas; i++){
        int beneficio;
        int contagio;
        cin >> beneficio;
        cin >> contagio;
        tiendas.push_back((make_tuple(beneficio, contagio)));
		//cout << get<0>(tiendas[i]) << '\n';
	}

	// Ejecutamos el algoritmo y obtenemos su tiempo de ejecución.
    int optimum = -1;
	std::chrono::_V2::steady_clock::time_point start;
    std::chrono::_V2::steady_clock::time_point end;
	if (algoritmo == "FB"){
        start = chrono::steady_clock::now();
		optimum = FB(0, true, 0,0, false);
        end = chrono::steady_clock::now();
	}
	else if (algoritmo == "BT"){
        start = chrono::steady_clock::now();
        int sumaMaxima=0;
        for(int i = 0; i<tiendas.size(); i++){
            sumaMaxima+=get<0>(tiendas[i]);
        }
        optimum = BT(0, 0, 0, false, sumaMaxima);
        end = chrono::steady_clock::now();
	}
	else if (algoritmo == "BT-F"){
        start = chrono::steady_clock::now();
		optimum = BTF(0, false, 0, 0);
        end = chrono::steady_clock::now();
	}
	else if (algoritmo == "BT-O"){
        start = chrono::steady_clock::now();
		int sumaMaxima=0;
        for(tuple<int, int> ti : tiendas){
            sumaMaxima+=get<0>(ti);
        }
		optimum = BTO(0, true, 0, 0, false, sumaMaxima);
        end = chrono::steady_clock::now();
	}
	else if (algoritmo == "DP"){
		// Precomputamos la solucion para los estados.
        //cout << get<0>(tiendas[cantTiendas-1]);
        start = chrono::steady_clock::now();
		vector<vector<int>> M(cantTiendas+1, vector<int>(contagioLimite+1, -1));


        // Matriz de cantTiendas filas, contagioLimite columnas iniciadas en -1.
		

         //for (int i = cantTiendas; i <= 0; i++)
		 	//for (int j = 0; j < contagioLimite+1;  j++)
			//	PD(i,j, M);
        optimum = PD(0, contagioLimite, M); // Obtenemos la solucion optima.
		
        end = chrono::steady_clock::now();
	}
	
	double total_time = chrono::duration<double, milli>(end - start).count();
    //cout << iteraciones << endl;
	// Imprimimos el tiempo de ejecución por stderr.
	clog << total_time << endl;

	// Imprimimos el resultado por stdout.
	cout << (optimum == -1 ? -1 : optimum) << endl;
	return 0;
}
