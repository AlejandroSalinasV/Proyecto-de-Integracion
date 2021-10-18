#ALGORITMO DE  QUINE-McCLUSKEY
#DESARROLLADO PARA ENCONTRAR LA SOLUCIÓN A UN CIRCUITO COMBINATORIO
#ALTERNATIVA A DIAGRAMAS  K
#ESPERO NO MORIR EN EL INTENTO :'V,
# 05-08-21


#CON BASE AL EJEMPLO https://www.youtube.com/watch?v=DTOzK88Inkk
# comprobar http://www.32x8.com/var4.html
#DESARROLLADO PARA 4 VARIABLES
#SUMA m(1,3,4,5,9,11,12,13,14,15)

# m     w   x   y   z   F
# 0     0   0   0   0   0
# 1     0   0   0   1   1
# 2     0   0   1   0   0
# 3     0   0   1   1   1
# 4     0   1   0   0   1
# 5     0   1   0   1   1
# 6     0   1   1   0   0
# 7     0   1   1   1   0
# 8     1   0   0   0   0
# 9     1   0   0   1   1
#10     1   0   1   0   0
#11     1   0   1   1   1 
#12     1   1   0   0   1
#13     1   1   0   1   1
#14     1   1   1   0   1
#15     1   1   1   1   1

#ESTADOS QUE SE DEBEN DE OBTENER A TRAVES DE ARDUINO


import math


#########----------------------------------------------------
#########----------------------------------------------------
#########---------------------------------------------------- 

#TABLA 1, CONSISTE EN CONTAR LA CANTIDAD DE 1's QUE SE TIENEN EN CADA ESTADO
def iteracion1(canonicos, estados, indices):
    cero=[]
    uno=[] # nombre del diccionario
    dos= []
    tres=[]
    cuatro=[]
    m_0=[]
    m_1=[] # miniterminos
    m_2=[]
    m_3=[]
    m_4=[]
    for i in range(len(canonicos)):
        unos=0
        for j in range(int(math.log(len(estados)+1,2))): #encuentra la cantidad de unos        
            if canonicos[i][j]== "1":
                unos=unos+1
        if unos == 0:
            cero.append(canonicos[i])
            m_0.append(indices[i])
        if unos == 1:
            uno.append(canonicos[i])
            m_1.append(indices[i])
        if unos == 2:
            dos.append(canonicos[i])
            m_2.append(indices[i])
        if unos == 3:
            tres.append(canonicos[i])
            m_3.append(indices[i])
        if unos == 4:
            cuatro.append(canonicos[i])
            m_4.append(indices[i])

    tabla1={"cero": [cero,m_0],
            "uno": [uno,m_1],
            "dos": [dos,m_2],
            "tres": [tres, m_3],
            "cuatro": [cuatro, m_4],}
    return tabla1

#########---------------------------------------------------- 
#########---------------------------------------------------- 
#########---------------------------------------------------- 
def iteracion2(tabla):
    #COMPARA EL NUMERO DE ELEMENTOS DE CADA GRUPO DE CANTIDAD DE BITS (1'S, 2'S, 3'S,4'S )
    # CON EL GRUPO SIGUIENTE, 1->2, 2->3, 3->4
    # Solo un bit puede diferir, si es asi coloca "-"
    #ENTRADA:
    #tabla1{"uno": [[binario], [indice]]}
    dim = [] # guardaremos el tamaño de cada arreglo
    keys=[] # guardamos la llave del diccionario 
    for key in tabla:
        dim.append(len(tabla[key][0]))
        keys.append(key)

    
    index = 0
    ####VARIABLES DONDE GUARDAREMOS DATOS DE ESTA SUBRUTINA
    cero=[]# nombre del diccionario
    uno=[] 
    dos= []
    tres=[]
    m_0=[]# miniterminos
    m_1=[] 
    m_2=[]
    m_3=[]
    
    nuevos=[]
    indices= []
    
    for i in range(len(keys)-1):
        
        for j in range(dim[index]):        
            aux1 = tabla[keys[i]][0][j]
            m = tabla[keys[i]][1][j]
            #print(f"Variable aux: {aux1}")
            #print(f"Indice : {m}")
            
            
            for k in range(dim[index+1]):
                diferencias = 0
                aux2 = tabla[keys[i+1]][0][k]
                m2 = tabla[keys[i+1]][1][k]
                aux3=[]
                for _ in range (numero_de_bits):
                    if aux1[_] != aux2[_]:
                        diferencias=diferencias+1                        
                        aux3+='-'
                    else:
                        aux3+=aux1[_]
                aux3 = ''.join(map(str,aux3)) # convertimos los caracteres a un string
                
                if diferencias == 1:
                    indices.append(m)
                    indices.append(m2)                    
                    if index == 1:
                        uno.append(aux3)
                        m_1.append(indices)
                        ##llenado[fill] = -1
                    elif index == 2: 
                        dos.append(aux3)
                        m_2.append(indices)
                        ##llenado[fill] = -1
                        
                    elif index==3:
                        tres.append(aux3)
                        m_3.append(indices)
                        ##llenado[fill] = -1
                    else:
                        cero.append(aux3)
                        m_0.append(indices)
                        
                    indices=[]
                #print(f" imprimiendo variable aux3: {aux3} en key: {i}, en k: {k}, dif. {diferencias}")
                
                    
            
            #comparar y guardar
        index = index +1 
        
    tabla2={"cero":[cero,m_0],
            "uno": [uno,m_1],
            "dos": [dos,m_2],
            "tres": [tres, m_3],}
    return tabla2

###**************************************************************###
#########----------------------------------------------------
#########----------------------------------------------------
#########---------------------------------------------------- 
def iteracion3(tabla):
    ''' COMBINAR GRUPOS 1 CON 2 Y 2 CON 3. MARCAR LOS TERMINOS
        QUE SE VAN INCLUYENDO Y EVITAR REPETICIONES!!!!!!

        ESTRUCTURA DE LA TABLA
        TABLA = {'KEY': [[GRUPOS][[INDICE1],[INDICE2]...]}
        TABLA = {'KEY': [[LISTA][[LISTA[LISTA]]]}
    '''
    
    dim = [] # guardaremos el tamaño de cada arreglo
    keys=[] # guardamos la llave del diccionario 
    for key in tabla:
        dim.append(len(tabla[key][0]))
        keys.append(key)

    
    index = 0
    ####VARIABLES DONDE GUARDAREMOS DATOS DE ESTA SUBRUTINA
    cero = []
    uno=[] # nombre del diccionario
    dos= []
    m_0=[]
    m_1=[] # miniterminos
    m_2=[]   
    
    nuevos=[]
    indices= []

    llenado = []
    for i in range(len(keys)-1):        
        for j in range(dim[index]):        
            aux1 = tabla[keys[i]][0][j]
            m = tabla[keys[i]][1][j]            
            
            for k in range(dim[index+1]):
                diferencias = 0
                aux2 = tabla[keys[i+1]][0][k]
                m2 = tabla[keys[i+1]][1][k]
                aux3=[]
                for _ in range (numero_de_bits):
                    if aux1[_] != aux2[_]:
                        diferencias=diferencias+1                        
                        aux3+='-'
                    else:
                        aux3+=aux1[_]
                aux3 = ''.join(map(str,aux3)) # convertimos los caracteres a un string
                if diferencias == 1:
                    #indices.append(m)
                    #indices.append(m2)                   
                
                    a = m
                    b = m2
                    c = a+b #concatenamos listas
                    c.sort() # ordenamos 
                    
                    indices = c
                    
                    try:
                        fill = llenado.index(c)
                    except:
                        fill = -1
                    #print(f"fill: {fill}")
                    llenado.append(c)
                    
                    #print(f"llenado: {llenado}")
                    if index == 0 and fill == -1:
                        cero.append(aux3)
                        m_0.append(indices)
                    elif index == 1 and fill == -1:
                        uno.append(aux3)
                        m_1.append(indices)
                        
                    elif index == 2 and fill == -1: 
                        dos.append(aux3)
                        m_2.append(indices)
                    
                        
                    
                    #print(f" imprimiendo variable aux3: {aux3} en key: {i}, en k: {k}, indices {indices}")   
                    indices=[]
                    
            #comparar y guardar
        index = index +1
        
    tabla3={"cero":[cero,m_0],
            "uno": [uno,m_1],
            "dos": [dos,m_2],}
    #print(f"Imprimiendo tabla3 {tabla3}")
    return tabla3
#########----------------------------------------------------
#########----------------------------------------------------
#########---------------------------------------------------- 
def no_repeticiones(data):
    result = []
    for item in data:
        if item not in result:
            result.append(item)        
    return result
#########----------------------------------------------------
#########----------------------------------------------------
#########---------------------------------------------------- 

def contar_veces(elemento, lista):
    
    veces = 0
    for i in lista:        
        if elemento == i:            
            veces += 1
    return veces
#########----------------------------------------------------
#########----------------------------------------------------
def letras(ecuacion):
    ecuacion_letras=[]
    dim_ecu_letras = len(ecuacion)
    for i in range(dim_ecu_letras):
        terminos=[]
        for j in range(len(ecuacion[i])):
            ####LETRA A
            if ecuacion[i][j]== '1' and j == 0:
                terminos+="A"
            if ecuacion[i][j]== '0' and j == 0:
                terminos+="A'"
            ####LETRA B
            if ecuacion[i][j]== '1' and j == 1:
                terminos+="B"
            if ecuacion[i][j]== '0' and j == 1:
                terminos+="B'"
            ####LETRA C
            if ecuacion[i][j]== '1' and j == 2:
                terminos+="C"
            if ecuacion[i][j]== '0' and j == 2:
                terminos+="C'"
            ####LETRA D
            if ecuacion[i][j]== '1' and j == 3:
                terminos+="D"
            if ecuacion[i][j]== '0' and j == 4:
                terminos+="D'"
        if i < dim_ecu_letras-1: 
            terminos+=' + '
            
        terminos = ''.join(map(str,terminos))
        ecuacion_letras+=terminos
    ecuacion_letras = ''.join(map(str,ecuacion_letras))
    return ecuacion_letras
#########---------------------------------------------------- 

def primos_implicantes(tabla):
    '''
    SE OBTENDRA LA SUMA MINIMA O LOS PRIMOS
    IMPLICANTES ESENCIALES.

    EN ESTE CASO SOLO SE REQUIERE DE LOS INDICES,
    LA FAMILIA DE PRIMOS IMPLICAS, BASTA CON QUE SOLO UN INDICE
    DE DICHA FAMILIA SE ENCUENTRE UNA VEZ. PARA QUE EL RESTO DE LA FAMILIA
    SEA UNA SUMA MINIMA.
    
    '''
    #print("FUNCION PRIMOS IMPLICANTES")
    dim = [] # guardaremos el tamaño de cada arreglo
    keys=[] # guardamos la llave del diccionario 
    for key in tabla:
        dim.append(len(tabla[key][0]))
        keys.append(key)
    #implicante = []
    #index = 0 # ya que solo evalua la familia de uno, y se tienen solo uno y dos.   
##    print(len(tabla[key][1][0]))
##    for i in range(len(keys)):        
##        for j in range(dim[index]):
##            for k in range(len(tabla[keys[i]][1][j])):
##                pibote1 = tabla[keys[i]][1][j][k]
##                # tenemos el pibote para comparar con los demas estados.
##                print(f"El pibote1 es {pibote1}")
    ###CALCULAMOS LOS INDICES TOTALES          
    index2 = 0
    total= 0
    tam = len(tabla[keys[1]][1][0])
    offset_inicial= 1
    indices_juntos=[]
    for l in range(len(keys)):                    
        for m in range(dim[index2]):
            for n in range(len(tabla[keys[l]][1][m])):
                pibote2= tabla[keys[l]][1][m][n]
                indices_juntos.append(pibote2)
                #print(f"El pibote2 es {pibote2}")
                total= total +1
        
        index2 = index2+1
    total_grupos= total//tam

    indices = []
    terminos = []
    index=0
    for l in range(len(keys)):                    
        for m in range(dim[index]):
            indices.append(tabla[keys[l]][1][m])
            terminos.append(tabla[keys[l]][0][m])
        index= index +1

    implicantes = []
    implicantes2 = []  
    for j in indices_juntos:
        b=contar_veces(j, indices_juntos)
        if b==1:
            implicantes.append(j)
    for i in implicantes:        
        a = indices_juntos.index(i)
        a = a//tam        
        implicantes2.append(a)
        
    ###resultado se tienen solos los esenciales, hace falta 
    resultado_indices=[]
    ecuacion = []
    for i in implicantes2:
        resultado_indices.append(indices[i])
        ecuacion.append(terminos[i])
    #####TENEMOS TODOS LOS IMPLICANTES ESENCIALES, FALTA OBTENER SU COMPLEMENTO
        #QUE SUME UN TOTAL DE LOS MINITERMINOS
    #ELIMINAMOS LOS IMPLICANTES DE LA LISTA DE IMPLICANTES
    index_implicantes=[]
    for i in range(len(resultado_indices)):
        for j in range(len(resultado_indices[0])):
            aux_pib = resultado_indices[i][j]
            index_implicantes.append(aux_pib)

    if len(index_implicantes) >= dim_indices:
        #print(ecuacion)
        ecuacion_letras = letras(ecuacion)
        print(ecuacion_letras)
        return ecuacion_letras

##    try:                 fill = llenado.index(c)
##                    except:
##                        fill = -1
    eliminar_indices=[]
    #eliminar_indices= indices_juntos.copy()
    
    eliminar_indices = no_repeticiones(indices_juntos.copy())
    
    for i in range(len(index_implicantes)):
        try:
            eliminar_indices.remove(index_implicantes[i])
        except:
            pass
    ###encontrar los indices restantes:
    restantes=[]
    for i in eliminar_indices:
        a = indices_juntos.index(i)
        a = a//tam 
        restantes.append(a)
    restantes = no_repeticiones(restantes)

    for i in restantes:
        resultado_indices.append(indices[i])
        ecuacion.append(terminos[i])
    
    ###calculamos los primos implicantes y a que familia pertenecen 
##    print(indices_juntos)
##    print(indices)
##    print(total_grupos)
##    print(implicantes)
##    print(implicantes2)
##    print(resultado_indices)
##    print(index_implicantes)
##    print(eliminar_indices)
##    print(restantes)
##    print(ecuacion)
    ecuacion_letras = letras(ecuacion)
    print(ecuacion_letras)
    #print(type(ecuacion[0][2]),ecuacion[0][2])
    return ecuacion_letras                
          
#########----------------------------------------------------
#########----------------------------------------------------

#########----------------------------------------------------
#########---------------------------------------------------- 

def ALGORITMO_McCLUSKEY(estados, salida):
    global dim_indices
    global numero_de_bits
    numero_de_bits= int(math.log(len(estados)+1,2))





    canonicos=[]
    indices= []
    for _ in range(len(salida)):
        if salida[_] == "1":
            indices.append(_)
            canonicos.append(estados[_])
    dim_indices = len(indices)
    #print(f"Estados canonicos: {canonicos}")
    #print(f"Indices: {indices}, tamaño de indices {dim_indices}")


    tabla1 = iteracion1(canonicos,estados, indices)
    #print(tabla1)

    #la estructura de la tabla 1, o primera iteracion es en diccionario, de la la siguiente forma:
    ## tabla1{"uno": [[binario], [indice]]}

    #print('ITERACION 2')
    tabla2=iteracion2(tabla1)
    #print(tabla2)

    #print('ITERACION 3')
    tabla3=iteracion3(tabla2)
    resultado=primos_implicantes(tabla3)
    return(resultado)

    #####NOTA IMPORTANTE!!!!!!
    #CONSIDERAR CUANDO SE TIENEN 0'S EN TOTAL

        
####*********************************************************### 
################INICIO DEL MAIN#################################
####*********************************************************###

#ESTADOS y SALIDAS QUE SE DEBEN DE OBTENER A TRAVES DE ARDUINO

###estados = ["0000","0001","0010", "0011",
##           "0100","0101","0110", "0111",
##           "1000","1001","1010", "1011",
##           "1100","1101","1110", "1111"]
##
###salida = ["0","0","1","1",
##          "1","1","1","1",
##          "1","0","1","0",
##          "1","1","1","1"]
#resultado=ALGORITMO_McCLUSKEY(estados,salida)
#print(resultado)

    #OBTENER VALORES CANONICOS
    #Valores donde la salida es 1



    






