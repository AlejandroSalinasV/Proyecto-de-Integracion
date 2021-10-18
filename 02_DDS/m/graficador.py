# *************************************
#
#   Clase: --> Graficador 
#   Modulo: -> graficador.py
#
# Descripción:
#   - Graficar los datos obtenidos por arduino
#   - Dibuar, mostrar informacion
#   - Calcular algunos parametros
#
# Fecha: Agosto 2/2021
#
# ************************************

import numpy as np
import cv2

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.image as img # libreria para mostrar esquematico


from collections import deque
import graphviz as gv

import math
import statistics

graficas = []


def draw( estados, inicio, trans, final):  # se quito alf, para no poner estado de 1  
    print("inicio:", str(inicio))
    #Se elige el formato del archivo
    g = gv.Digraph(format='svg')
    g.graph_attr['rankdir'] = 'LR'
    g.unflatten(stagger=3)
    #genera el punto
    g.node('ini', shape="point")
    for e in estados:
        if e in final:            
            g.node(e, shape="doublecircle")
        else:
            g.node(e)
        #quita el estado inicial, la flecha
        if e in inicio:
            g.edge('ini',e)

    for t in trans:
        #if t[2] not in alfabeto:
            #return 0
        g.edge(t[0], t[1])
        
    g.attr(label=r'\n\nDIAGRAMA DE ESTADOS') #Colocar un titulo a la imagen
    g.attr(fontsize='20')
    
    g.render(view=True) #ULTIMA LINEA PARA VIZUALIZAR

class Graficador():

    # -------------------------------------------------------
    #           CONSTRUCTOR
    # -------------------------------------------------------
    def __init__(self,modelo):

        print("")
        print(" CONSTRUCTOR:  Clase: Graficador")
        self.modelo = modelo
        self.vectores_muestras = modelo.vectores_muestras
        self.titulos_vectores_muestras = modelo.titulos_vectores_muestras
        self.titulos_marcadores_display = modelo.titulos_marcadores_display

    def construir_graficas_muestras(self):

        # --- Construccion AUTOMATICA de la graficas ---
        titulos_marcadores = list(self.titulos_marcadores_display)
            
        global graficas
        graficas = []

        muestras = self.vectores_muestras

        for i in range(len(titulos_marcadores)):
            titulo_grafica = self.titulos_marcadores_display[titulos_marcadores[i]]
            nombre_vectores_grafica = self.extraer_informacion_cadena(titulo_grafica)

            # --- Construccion AUTOMATICA de cada GRAFICA, a partir de la
            #     información proporcionada en la clase Modelo en las estructuras:
            #     -> titulos_vectores_muestras   <-- Vector
            #     -> titulos_marcadores_display  <-- Diccionario
            #     Estas estructuras de datos se conectan con los nombres de los
            #     vectores que se encuentran en el Diccionario muestras
            #     -> vectores_muestras <-- Diccionario
            # --------------------------------------------------------------------
            plt.figure(i)
            # --- Graficas VECTOR A vs. muestras ---
            if len(nombre_vectores_grafica) == 1 and len(nombre_vectores_grafica[0]) == 1:
                plt.plot(muestras[nombre_vectores_grafica[0][0]],
                         label = nombre_vectores_grafica[0][0] + ' vs. muestras')
            # --- Graficas VECTOR A vs VECTOR B ---
            if len(nombre_vectores_grafica) == 1 and len(nombre_vectores_grafica[0]) == 2:
                plt.plot(muestras[nombre_vectores_grafica[0][0]],
                         muestras[nombre_vectores_grafica[0][1]],
                         label = nombre_vectores_grafica[0][0] + ' vs. ' +
                         nombre_vectores_grafica[0][1])
            # --- Graficas MULTIPLES tipo: VECTOR A vs VECTOR B ---
            if len(nombre_vectores_grafica) > 2:
                for g in range(len(nombre_vectores_grafica)):
                    plt.plot(muestras[nombre_vectores_grafica[g][0]],
                             muestras[nombre_vectores_grafica[g][1]],
                             label = nombre_vectores_grafica[g][0] + ' vs. ' +
                             nombre_vectores_grafica[g][1])    
            plt.titulo = 'Grafica ' + str(i)
            plt.ylabel = 'y label'
            plt.xlabel = 'x label'
            plt.legend()
            
            # --- Guardado de las gráficas en:
            #     1. "Archivo en disco [*.jpg] para su uso posterior
            #        por parte de la Clase Display
            #     2. El arreglo GLOBAL: 'graficas', elcual contiene
            #        la ruta en donde se guardó la gráfica correspondiente
            # ------------------------------------------------------------
            grafica = 'g/grafica_' + str(i) + ".jpg"
            plt.savefig(grafica)
            graficas.append(grafica)

    def extraer_informacion_cadena(self,cadena):

        #print("")
        #print(" cadena original = ",cadena)

        # --- Separa grupos de letras ---
        subcadena = ''
        subtitulos = []
        ignorar_caracter = False
        num_char = 0
        for ch in cadena:
            num_char += 1
            # --- Ignorar los caracteres "espacio" [' '] y "coma" [','] ---
            if ch == ' ' or ch == ',':
                ignorar_caracter = True
                if num_char != 1:
                    subtitulos.append(subcadena)
                subcadena = ''
            else:
                subcadena += ch
            if num_char == len(cadena): subtitulos.append(subcadena)

        # --- Genera tuplas de dos elementos ---
        tupla = []
        arreglo_tuplas = []
        for i in range(len(subtitulos)):
            # --- Detecta conector ['vs'] ó espacio [' '] --
            if subtitulos[i] == 'vs' or subtitulos[i] == '':
                dummy = 0 # <--- No hacer nada ---
            else:
                tupla.append(subtitulos[i])
            if subtitulos[i] == '' or i == (len(subtitulos)-1):
                arreglo_tuplas.append(tupla)
                tupla = []
                
        return arreglo_tuplas

    def graficar_curvas_DDS(self):

        global graficas
        graficas = []

        muestras = self.vectores_muestras
##        titulos_vectores_muestras = self.titulos_vectores_muestras
##        muestras_llaves = list(muestras)
##        lim_max = len(muestras[muestras_llaves[0]])
##        sel_filtro = 1

        ##VARIABLES PARA LA GRAFICACIÓN ####
        frecuencia = muestras['Frecuencia'][0][0]
        periodo = round(1/frecuencia, 2)
        maximo = max(muestras['Voltaje'][0])
        minimo = min(muestras['Voltaje'][0])
        Binario = ["0000", "0001", "0010", "0011",
                   "0100", "0101", "0110", "0111",
                   "1000", "1001", "1010", "1011",
                   "1100", "1101", "1110", "1111"]
        
        Hex =     ["0x0", "0x1", "0x2", "0x3",
                   "0x4", "0x5", "0x6", "0x7",
                   "0x8", "0x9", "0xA", "0xB",
                   "0xC", "0xD", "0xE", "0xF"]
        voltaje =[]
        tiempo = []
        for i in range (17):
            voltaje.append(muestras['Voltaje'][0][i])
            tiempo.append(muestras['Tiempo'][0][i])
##            print(f"Voltaje: {voltaje[i]}")
##            print(f"Tiempo: {tiempo[i]}")
##            print(f"Binario: {Binario[i]}")

            
        # --- Grafica 0 : Voltaje en tiempo ---
        plt.figure(0)

        plt.ylim(minimo-1,maximo+1)
        plt.title("Voltaje en el tiempo")
        plt.plot(muestras['Tiempo'][0],muestras['Voltaje'][0],
                 label='Señal, $V_{max}$ = '+str(maximo)+
                 ' V, $V_{min}$ = '+str(minimo)+ " V," +
                 'F = ' + str(frecuencia) + 'Hz, '+
                 'T = ' + str(periodo) + 's'                 )
        plt.ylabel('Voltaje [V]')
        plt.xlabel('Tiempo [s]')
        plt.legend()
        
        grafica = 'g/grafica0' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
        
        # --- Grafica 1 : Valores de la señal ---
        plt.figure(1)
        plt.ylim(minimo-1,maximo+2)
        delta_tiempo = tiempo[1]/2
        plt.xlim(min(tiempo) - delta_tiempo, max(tiempo) + delta_tiempo)        
        plt.title("Valores de la señal en el tiempo")
        plt.plot(tiempo,voltaje,'o-',
                 label='Señal, $V_{max}$ = '+str(max(voltaje))+
                 ' V, $V_{min}$ = '+str(min(voltaje))+ " V," +
                 'F = ' + str(frecuencia) + 'Hz, '+
                 'T = ' + str(periodo) + 's'                 )
        plt.ylabel('Voltaje [V]')
        plt.xlabel('Tiempo [s]')
        index_temp = 1
        for x,y,z in zip(tiempo,voltaje,Binario):
            if index_temp<9:                
                delta_tiempo = -tiempo[1]/2
            #elif index_temp ==9:
             #   delta_tiempo = 0
            else:
                delta_tiempo = 0
                #delta_tiempo = tiempo[1]/2
            index_temp = index_temp +1
            plt.text(x + delta_tiempo, y, str(y) + "V\n"+str(z),fontsize=9 )
            
        plt.legend()  
        grafica = 'g/grafica1' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
        
        
        # --- Grafica 2 : Estados logicos ---

        #GENERAMOS SVG EN EL NAVEGADOR DE ESTADOS. POSTERIORMENTE
        #SE GENERA EL CANVAS
        plt.figure(2)
        
        estados = []
        for i in range(16): #ESTADOS QUE SE TIENEN
            estados.append(str(Binario[i])+"\n"+str(voltaje[i])+"V")        

        #SECUECNIA QUE SIGUEN A->B, B->C...
        trans = [(estados[0],estados[1]),
                 (estados[1],estados[2]),
                 (estados[2],estados[3]),
                 (estados[3],estados[4]),
                 (estados[4],estados[5]),
                 (estados[5],estados[6]),
                 (estados[6],estados[7]),
                 (estados[7],estados[8]),
                 (estados[8],estados[9]),
                 (estados[9],estados[10]),
                 (estados[10],estados[11]),
                 (estados[11],estados[12]),
                 (estados[12],estados[13]),
                 (estados[13],estados[14]),
                 (estados[14],estados[15]),                 
                 (estados[15],estados[0])]
        
        #trans = []
        inicial = [estados[0]]        
        terminal = (estados[15],)

        #draw(alf, estados, inicial, trans, terminal)
        draw(estados, inicial, trans, terminal) # se quito alf para no poner estado de 1 y 0


        
        

        # --- Grafica DE ESTADOS---
        ##CODIGO DE FERNANDO REUTILIZADO.
        
        
        canvas2 = np.ones((480,640,3), dtype = "uint8")*255
        
        # --- RECTANGULO ---
        cv2.rectangle(canvas2, (20,20),(620,40),(0,0,0), -1, cv2.LINE_AA)

        # --- Estados binarios ---
        
        cv2.putText(canvas2,"Diagrama de numeros binarios con valores de voltaje analogicos",
                    (30, 35),cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1, cv2.LINE_AA)
        #cv2.circle(canvas2, (320,260), 215,(255,0,0),2)
        #cv2.circle(canvas2, (320,260), 185,(255,0,0),2)

        angle = np.linspace(0,2*math.pi,17)

        # Dibuja cada uno de los circulos y la informacion voltaje-binario que va dentro de ella. Tambien dibuja las flechas entre circulos
        for i in range(0,16):
            # Dibuja el circulo            
            xcoor = int(320+185*math.cos(angle[i]))
            ycoor = int(260+185*math.sin(angle[i]))
            if i == 0:
                cv2.circle(canvas2, (xcoor,ycoor), 30, (0,0,255), 2) ## Color en BGR
            else:
                cv2.circle(canvas2, (xcoor,ycoor), 30, (0,0,0), 2)               
            
            cv2.putText(canvas2,str(Binario[i]),(xcoor-22,ycoor-5),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(canvas2,str(voltaje[i])+'V',(xcoor-22,ycoor+15),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 1, cv2.LINE_AA)

            # Encuentra las coordenadas de la flecha entre dos circulos
            i1 = self.get_intersections(320,260,185,xcoor,ycoor,30)
            i2 = self.get_intersections(320,260,185,int(320+185*math.cos(angle[i+1])),int(260+185*math.sin(angle[i+1])),30)
            dist = 100
            flecha_coords = [0]*4
            '''for j in range(0,1):
                if math.dist([i1[j*2],i1[j*2+1]],[i2[j*2],i2[j*2+1]]) < dist:
                    print("1, j="+str(j))
                    dist = math.dist([i1[j*2],i1[j*2+1]],[i2[j*2],i2[j*2+1]])
                    flecha_coords[0] = i1[j*2]
                    flecha_coords[1] = i1[j*2+1]
                    flecha_coords[2] = i2[j*2]
                    flecha_coords[3] = i2[j*2+1]
                if math.dist([i1[(2-j*2)],i1[(2-j*2)+1]],[i2[j*2],i2[j*2+1]]) < dist:
                    print("2, j="+str(j))
                    dist = math.dist([i1[j*2],i1[j*2+1]],[i2[j*2],i2[j*2+1]])
                    flecha_coords[0] = i1[(2-j*2)]
                    flecha_coords[1] = i1[(2-j*2)+1]
                    flecha_coords[2] = i2[j*2]
                    flecha_coords[3] = i2[j*2+1]'''
            # Se puede comprobar con el codigo comentado que esta es la solucion que proporciona las coordenadas correctas
            flecha_coords[0] = i1[2]
            flecha_coords[1] = i1[3]
            flecha_coords[2] = i2[0]
            flecha_coords[3] = i2[1]
            
            #print('coordenadas de la flecha: '+str(flecha_coords))
            #print('distancia: '+str(dist))

            # Dibuja la flecha
            canvas2 = cv2.arrowedLine(canvas2,(int(flecha_coords[0]),int(flecha_coords[1])),(int(flecha_coords[2]),int(flecha_coords[3])),(0,0,0), 3, tipLength = 0.5)

        grafica = 'g/grafica2' + ".jpg"        
        cv2.imwrite(grafica,canvas2)
        graficas.append(grafica)

        
        # --- Grafica 3: DIAGRAMA DEL CIRCUITO ---
        plt.figure(3)
        diagrama = img.imread('i/DDS_bb.png')
        plt.imshow(diagrama)
        grafica = 'g/grafica3' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
        
        # --- Auxiliar para depuracion ---
        #plt.show()        

    @property
    def graficas(self):
        return graficas # --- Nombre de la grafica y ruta donde se guardo ---

    def imprimir_archivos_graficas(self):

        print(" ")
        print(" En CLASE Graficador::")
        print("**************************************************")
        print("   --- Archivos de imagenes de graficas *.jpg ---")
        print("**************************************************")
        for g in graficas:
            print("")
            print(g)
  
    def imprimir_muestras_canal(self):

        print(" ")
        print(" En CLASE Graficador::")
        print("**************************************************")
        print("      --- Vectores de muestras por canal ---")
        print("**************************************************")
        # --- ESTRUCTURA del diccionario:
        #     datos = {canal: i, llaveMuestras[i]: vector de datos}
        # ---------------------------------------------------------
        muestras = self.vectores_muestras
        llaves = list(muestras)
        print(" llaves = ",llaves)
        for k in range(len(llaves)):
            print("")
            print(" --- ",llaves[k],": ",muestras[llaves[k]])

    def imprimir_vectores_muestras(self):

        print(" ")
        print(" En CLASE Graficador::")
        print("**************************************************")
        print(" -- Muestras leidas de la Clase Modelo --")
        print("**************************************************")
        muestras = self.vectores_muestras
        llaves = self.titulos_vectores_muestras
        print(" llaves = ",llaves)
        for k in range(len(llaves)):
            print("")
            print(" --- ",llaves[k],": ",muestras[llaves[k]])

    # -------------------------------------------------------
    # Obtiene las intersecciones dadas dos circunferencias, coordenadas de su centro y radio. 
    # Tomado de https://stackoverflow.com/questions/55816902/finding-the-intersection-of-two-circles
    # -------------------------------------------------------
    def get_intersections(self, x0, y0, r0, x1, y1, r1):
        # circle 1: (x0, y0), radius r0
        # circle 2: (x1, y1), radius r1

        d = math.sqrt((x1-x0)**2 + (y1-y0)**2)
        
        # non intersecting
        if d > r0 + r1 :
            return None
        # One circle within other
        if d < abs(r0-r1):
            return None
        # coincident circles
        if d == 0 and r0 == r1:
            return None
        else:
            a=(r0**2-r1**2+d**2)/(2*d)
            h=math.sqrt(r0**2-a**2)
            x2=x0+a*(x1-x0)/d   
            y2=y0+a*(y1-y0)/d   
            x3=x2+h*(y1-y0)/d     
            y3=y2-h*(x1-x0)/d 

            x4=x2-h*(y1-y0)/d
            y4=y2+h*(x1-x0)/d
            
            return (x3, y3, x4, y4)

    
            
        
