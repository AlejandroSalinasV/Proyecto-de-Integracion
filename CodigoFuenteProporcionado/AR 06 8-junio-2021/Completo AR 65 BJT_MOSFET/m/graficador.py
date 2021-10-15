# *************************************
#
#   Clase: --> Graficador 
#   Modulo: -> graficador.py
#
# Descripción:
#   - Graficar los datos obtenidos por arduino
#   - Dibuar, mostrar informacion
#
# Fecha: abril 13/2021
#
# ************************************

import numpy as np
import cv2

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from collections import deque

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

    def graficar_curvas_BJT(self):

        global graficas
        graficas = []

        muestras = self.vectores_muestras
                
        # --- Grafica 0 : Ic vs Vce ---
        plt.figure(0)
        plt.plot(muestras['Vbe'][5], muestras['Ic'][5], label='Ic vs Vbe')
        #plt.ylim(0,5)
        plt.xlim(0,1)   # <- BJT
        #plt.xlim(0,3)  # <- MOSFET
        plt.xlabel('Vbe (V)')
        plt.ylabel('Ic (mA)')
        plt.title("Ic vs Vbe")
        plt.legend()
        grafica = 'g/grafica_0' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 1: Ib vs Vbe ---
        plt.figure(1)
        plt.plot(muestras['Vbe'][5], muestras['Ib'][5], label='Ib vs Vbe')
        #plt.ylim(0,20)
        plt.xlim(0,1)
        plt.xlabel('Vbe (V)')
        plt.ylabel('Ib (uA)')
        plt.title("Ib vs Vbe")
        plt.legend()
        grafica = 'g/grafica_1' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        
        # --- Grafica 2: Ic vs Vce (Cinco curvas sin promediar) ---
        plt.figure(2)
        for i in range(len(muestras['Ic'])-1):
            label_Vbe=str((int(np.average(muestras['Vbe'][i])*1000))/1000)
            label_Ib=str((int(np.average(muestras['Ib'][i])*1000))/1000)
            plt.plot(muestras['Vce'][i],muestras['Ic'][i],
                     label='Vbe='+label_Vbe+'v, Ib ='+label_Ib+' uA')
           
        plt.xlabel('Vce (V)')
        plt.ylabel('Ic (mA)')
        plt.title("Ic vs Vce")
        plt.legend()
        grafica = 'g/grafica_2' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 3 : Ic vs Vbe [PROMEDIADO - CIRCULAR] ---
        plt.figure(3)
        plt.plot(muestras['Vbe_pc'][5], muestras['Ic_pc'][5], label='Ic vs Vbe')
        plt.xlim(0,1)   # <- BJT
        #plt.xlim(0,3)  # <- MOSFET
        plt.xlabel('Vbe (V)')
        plt.ylabel('Ic (mA)')
        plt.title("Ic vs Vbe [pc]")
        plt.legend()
        grafica = 'g/grafica_3' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 4: Ib vs Vbe [PROMEDIADO - CIRCULAR] ---
        plt.figure(4)
        plt.plot(muestras['Vbe_pc'][5], muestras['Ib_pc'][5], label='Ib vs Vbe')
        plt.xlim(0,1)
        plt.xlabel('Vbe (V)')
        plt.ylabel('Ib (uA)')
        plt.title("Ib vs Vbe [pc]")
        plt.legend()
        grafica = 'g/grafica_4' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
        
        # --- Grafica 5: Ic vs Vce (5 curvas)[PROMEDIADO - CIRCULAR] ---
        plt.figure(5)
        for i in range(len(muestras['Ic_pc'])-1):
            label_Vbe=str((round(np.average(muestras['Vbe_pc'][i])*1000))/1000)
            label_Ib=str((round(np.average(muestras['Ib_pc'][i])*1000))/1000)
            plt.plot(muestras['Vce_pc'][i],muestras['Ic_pc'][i],
                     label='Vbe='+label_Vbe+'v, Ib ='+label_Ib+' uA')
        plt.xlabel('Vce (V)')
        plt.ylabel('Ic (mA)')
        plt.title("Ic vs Vce [pc]")
        plt.legend()
        grafica = 'g/grafica_5' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 6: Ic vs Vce (5 curvas)[PROMEDIADO - LowPass - 8] ---
        plt.figure(6)
        for i in range(len(muestras['Ic_lp'])-1):
            label_Vbe=str((round(np.average(muestras['Vbe_lp'][i])*1000))/1000)
            label_Ib=str((round(np.average(muestras['Ib_lp'][i])*1000))/1000)
            plt.plot(muestras['Vce_lp'][i],muestras['Ic_lp'][i],
                     label='Vbe='+label_Vbe+'v, Ib ='+label_Ib+' uA')
        plt.xlabel('Vce (V)')
        plt.ylabel('Ic (mA)')
        plt.title("Ic vs Vce [lp]")
        plt.legend()
        grafica = 'g/grafica_6' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 7: Ic vs Vbe [PROMEDIADO - LowPass] ---
        plt.figure(7)
        for i in range(len(muestras['Ic'])-1):
            label_Vbe=str((round(np.average(muestras['Vbe'][i])*1000))/1000)
            label_Ib=str((round(np.average(muestras['Ib'][i])*1000))/1000)
            plt.plot(muestras['Vce'][i],muestras['Ic'][i],
                     label='Vbe='+label_Vbe+'v, Ib ='+label_Ib+' uA')
            label_Vbe=str((round(np.average(muestras['Vbe_pc'][i])*1000))/1000)
            label_Ib=str((round(np.average(muestras['Ib_pc'][i])*1000))/1000)
            plt.plot(muestras['Vce_pc'][i],muestras['Ic_pc'][i],
                     label='pVbe='+label_Vbe+'v, Ib ='+label_Ib+' uA')
        plt.xlabel('Vce (V)')
        plt.ylabel('Ic (mA)')
        plt.title("Ic vs Vce [m]")
        plt.legend()
        grafica = 'g/grafica_7' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Auxiliar para depuracion ---
        #plt.show()        

    def graficar_curvas_MOSFET(self):

        global graficas
        graficas = []

        muestras = self.vectores_muestras
                
        # --- Grafica 0 : Id vs Vds ---
        plt.figure(0)
        plt.plot(muestras['Vgs'][5], muestras['Id'][5], label='Id vs Vds')
        #plt.ylim(0,5)
        plt.xlim(0,1)   # <- BJT
        #plt.xlim(0,3)  # <- MOSFET
        plt.xlabel('Vgs (V)')
        plt.ylabel('Id (mA)')
        plt.title("Id vs Vds")
        plt.legend()
        grafica = 'g/grafica_0' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 1: Ib vs Vbe ---
        plt.figure(1)
        plt.plot(muestras['Vgs'][5], muestras['Ig'][5], label='Ig vs Vgs')
        #plt.ylim(0,20)
        plt.xlim(0,1)
        plt.xlabel('Vgs (V)')
        plt.ylabel('Ib (uA)')
        plt.title('Ig vs Vgs')
        plt.legend()
        grafica = 'g/grafica_1' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        
        # --- Grafica 2: Ic vs Vce (Cinco curvas sin promediar) ---
        plt.figure(2)
        for i in range(len(muestras['Id'])-1):
            label_Vgs=str((int(np.average(muestras['Vgs'][i])*1000))/1000)
            plt.plot(muestras['Vds'][i],muestras['Id'][i],
                     label='Vgs='+label_Vgs+'v')
           
        plt.xlabel('Vds (V)')
        plt.ylabel('Id (mA)')
        plt.title('Id vs Vds')
        plt.legend()
        grafica = 'g/grafica_2' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 3 : Id vs Vds [PROMEDIADO - CIRCULAR] ---
        plt.figure(3)
        plt.plot(muestras['Vgs_pc'][5], muestras['Id_pc'][5], label='Id vs Vds')
        plt.xlim(0,1)   # <- BJT
        #plt.xlim(0,3)  # <- MOSFET
        plt.xlabel('Vgs (V)')
        plt.ylabel('Id (mA)')
        plt.title("Id vs Vds [pc]")
        plt.legend()
        grafica = 'g/grafica_3' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 4: Ib vs Vbe [PROMEDIADO - CIRCULAR] ---
        plt.figure(4)
        plt.plot(muestras['Vgs_pc'][5], muestras['Ig_pc'][5], label='Ig vs Vgs')
        plt.xlim(0,1)
        plt.xlabel('Vgs (V)')
        plt.ylabel('Ig (uA)')
        plt.title("Ib vs Vbe [pc]")
        plt.legend()
        grafica = 'g/grafica_4' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
        
        # --- Grafica 5: Ic vs Vce (5 curvas)[PROMEDIADO - CIRCULAR] ---
        plt.figure(5)
        for i in range(len(muestras['Id_pc'])-1):
            label_Vgs=str((round(np.average(muestras['Vgs_pc'][i])*1000))/1000)
            plt.plot(muestras['Vds_pc'][i],muestras['Id_pc'][i],
                     label='Vgs='+label_Vgs+'v')
        plt.xlabel('Vds (V)')
        plt.ylabel('Id (mA)')
        plt.title('Id vs Vds [pc]')
        plt.legend()
        grafica = 'g/grafica_5' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 6: Ic vs Vce (5 curvas)[PROMEDIADO - LowPass - 8] ---
        plt.figure(6)
        for i in range(len(muestras['Ic_lp'])-1):
            label_Vgs=str((round(np.average(muestras['Vgs_lp'][i])*1000))/1000)
            plt.plot(muestras['Vds_lp'][i],muestras['Ic_lp'][i],
                     label='Vgs='+label_Vgs+'v,')
        plt.xlabel('Vds (V)')
        plt.ylabel('Id (mA)')
        plt.title('Id vs Vds [lp]')
        plt.legend()
        grafica = 'g/grafica_6' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 7: Id vs Vds [PROMEDIADO - LowPass] ---
        plt.figure(7)
        for i in range(len(muestras['Id'])-1):
            label_Vgs=str((round(np.average(muestras['Vgs'][i])*1000))/1000)
            plt.plot(muestras['Vds'][i],muestras['Id'][i],
                     label='Vgs='+label_Vgs+'v')
            label_Vgs=str((round(np.average(muestras['Vgs_pc'][i])*1000))/1000)
            plt.plot(muestras['Vce_pc'][i],muestras['Id_pc'][i],
                     label='pVbe='+label_Vgs+'v')
        plt.xlabel('Vds (V)')
        plt.ylabel('Id (mA)')
        plt.title("Id vs Vds [m]")
        plt.legend()
        grafica = 'g/grafica_7' + ".jpg"
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

            

         
