# *************************************
#
#   Clase: --> Graficador 
#   Modulo: -> graficador.py
#
# Descripción:
#   - Graficar los datos obtenidos por arduino
#   - Dibujar, mostrar informacion
#
# Fecha: julio 28/2021
#
# ************************************


import numpy as np
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
#import matplotlib.image as img # libreria para mostrar imagenes
import m.McCluskey 

from collections import deque


import math


graficas = []

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

    


    def graficar_curvas_FSM(self):

        global graficas
        graficas = []

        muestras = self.vectores_muestras
        titulos_vectores_muestras = self.titulos_vectores_muestras
        muestras_llaves = list(muestras)
        #print('muestras_llaves: '+str(muestras_llaves))
        
        # Se obtiene el numero de series de muestras para cada canal (ej. para 300 muestras hay 6 curvas). 
        
        


        # --- Grafica 0 : Entrada, Estado y Salida en el tiempo ---------------------------------------------------------------------------------------
        plt.figure(0)
            
        print(muestras)
        for i in range(0,len(muestras_llaves)):
            print("MUESTAS LLAVE \n", muestras[muestras_llaves[i]])
        print(type(muestras))
        
        colores_lineas = ['tab:blue','tab:green']
        salidas=[]
        for i in range(len(muestras["salida"])):
            salidas.append(str(round(muestras["salida"][i])))
        
        #añadimos a las muestras el valor de  0 al estado 16 ya que sale incompleto
        muestras["salida"].append(muestras["salida"][-1])
        muestras["entrada"].append(muestras["entrada"][-1])
        
        lim_max = len(muestras[muestras_llaves[0]])
        for i in range(0,len(muestras_llaves)):
            plt.subplot(2, 1, i+1)           
            
            # Se grafican entrada, estado y salida. 
            plt.step(range(0,lim_max),muestras[muestras_llaves[i]], linewidth = 2,color=colores_lineas[i], where='post', label=muestras_llaves[i])

            # Se modifican los ejes para que muestren cada numero entero. 
            plt.xticks(np.arange(0,len(muestras[muestras_llaves[i]]),step = 1))
            plt.yticks(np.arange(0,max(muestras[muestras_llaves[i]]),step = 1))
            
            plt.ylabel(muestras_llaves[i])
            plt.legend()
            if i == 0:
                plt.title("ESTADOS COMBINATORIOS")
            
        plt.xlabel('MUESTRA') 
        grafica = 'g/00' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
        # --- Grafica 1: DIAGRAMA DEL CIRCUITO ---
        plt.figure(1)
        estados = ["0000","0001","0010", "0011",
                   "0100","0101","0110", "0111",
                   "1000","1001","1010", "1011",
                   "1100","1101","1110", "1111"]
        #VARIABLE salidas
        
        print(f"ESTAS SON LAS SALIDAS{salidas}")

        dt =  {'ABCD':estados,'F':salidas}
        cuadro = pd.DataFrame(data=dt)
        cuadro = cuadro.to_string(index= False,justify = 'center',col_space=16)
        img = Image.open("i/pizarra.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial",60)
        draw.multiline_text((100, 400),cuadro,(255,255,255),font=font,align='center')
        img.save('i/estados.jpg')
        
        
        plt.imshow(img)
        grafica = 'g/01' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        ###------
        plt.figure(2)
        resultado=m.McCluskey.ALGORITMO_McCLUSKEY(estados,salidas)
        rs=[]
        rs.append(resultado)
        dt =  {'POSIBLE RESPUESTA':rs}
        cuadro = pd.DataFrame(data=dt)
        cuadro = cuadro.to_string(index= False,justify = 'center',col_space=16)
        img2 = Image.open("i/pizarra.jpg")
        draw = ImageDraw.Draw(img2)
        font = ImageFont.truetype("arial",100)
        draw.multiline_text((100, 400),cuadro,(255,255,255),font=font,align='center')
        img.save('i/resultado.jpg')      
        
        
        plt.imshow(img2)
        grafica = 'g/02' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
        
        
              

        
        

        # --- Auxiliar para depuracion ---
        plt.show()
    
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
