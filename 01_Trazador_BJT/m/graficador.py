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
import matplotlib.image as img # libreria para mostrar esquematico

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

        ## --- SECCION DE GRAFICAS Y DATOS DEL TRANSISTOR --

        # --- Grafica 0: Ib vs Vbe [PROMEDIADO - LowPass] LP ---
        plt.figure(0)
        label_VbeON = 0.0
        contador_VbeON = 0; 
        for i in range(len(muestras['Vbe_lp'][5])):
            if  muestras['Ic_lp'][5][i] > 1.0:
                label_VbeON += muestras['Vbe_lp'][5][i]
                contador_VbeON += 1
                
        label_VbeON = str(round(label_VbeON / contador_VbeON, 3))
         
        plt.plot(muestras['Vbe_lp'][5], muestras['Ib_lp'][5],
                 label='$I_b$ vs $V_{be}$, $V_{be ON}$ = ' + label_VbeON + " V")
        plt.xlim(0,1)
        plt.xlabel('$V_{be}$ [V]')
        plt.ylabel('$I_b$ [$\\mu$A]')
        plt.title("$I_b$ vs $V_{be}$ ")
        plt.legend()
        grafica = 'g/grafica_0' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
                
        # --- Grafica 1 : Ic vs Vbe [PROMEDIADO - CIRCULAR]  ---
        plt.figure(1)
        plt.plot(muestras['Vce_pc'][5], muestras['Ic_pc'][5],
                 label='$I_c$ vs $V_be$, $V{be_ON}$ = ' + label_VbeON + " V")
        #plt.xlim(0,1)   # <- BJT        
        plt.xlabel('$V_{be}$ [V]')
        plt.ylabel('$I_c$ [mA]')
        plt.title("$I_c$ vs $V_{be}$")
        plt.legend()
        grafica = 'g/grafica_1' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
                


        # --- Grafica 2 : Ic vs Vbe [PROMEDIADO - LowPass] ---
        plt.figure(2)
        for i in range(len(muestras['Ic_lp'])-1):
            label_Vbe_lp= str(round(np.average(muestras['Vbe_lp'][i])+0.00001,3)) #Agregamos una constante sumamente pequeña, para truncar siempre a 3 cifras
            label_Ib_lp=  str(round(np.average(muestras['Ib_lp'][i] )+0.00001,3))
            label_Ic_lp=  str(round((muestras['Ic_lp'][i][3]+ muestras['Ic_lp'][i][2]+muestras['Ic_lp'][i][1])/3 + 0.000000000001, 3))
            plt.plot(muestras['Vce'][i],muestras['Ic'][i],
                     label='$V_{be}$='+label_Vbe_lp+' V, $I_b$ ='+label_Ib_lp+' $\\mu$A, $I_c$ = ' + label_Ic_lp + ' mA')
        plt.plot(muestras['Vce'][5],muestras['Ic'][5])
        plt.ylim(0,17) 
        plt.xlabel('$V_{ce}$ [V]')
        plt.ylabel('$I_c$ [mA]')
        plt.title("$I_c$ vs $V_{ce}$")
        plt.legend(loc='upper left')
        grafica = 'g/grafica_2' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 3: Beta vs Ic [PROMEDIADO - LowPass] ---
        plt.figure(3)
        # Beta = Ic / Ib
        Ic = []
        Ib = []
        Beta = []
        for i in range(len(muestras['Ic_lp'])-1):
            Ic.append(round((muestras['Ic_lp'][i][3]+ muestras['Ic_lp'][i][2]+muestras['Ic_lp'][i][1])/3 + 0.000000000001, 3))
            Ib.append(round(np.average(muestras['Ib_lp'][i] )+0.00001,3))
            Beta.append(round (Ic[i] * 1000/ Ib[i]))
        Beta_promedio = round(np.average(Beta)) 
                        
        plt.plot(Ic, Beta, 'o-', label='$\\beta$ vs $I_c$, $\\beta_{promedio}$ = ' + str(Beta_promedio))
        plt.ylim(min(Beta) - 20 ,max(Beta) + 20)
        plt.xlim(min(Ic) - 0.5 , max(Ic) + 0.5)
        for x,y in zip(Ic,Beta):
            plt.text(x-0.2, y - 1, str(y))
        
        plt.xlabel('$I_c$ [mA]')
        plt.ylabel('$\\beta$')
        plt.title("$\\beta$ vs $I_c$")
        plt.legend()
        grafica = 'g/grafica_3' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
         


        # --- Grafica 4: gm vs Ic (5 curvas)[PROMEDIADO - LowPass] ---
        plt.figure(4)
        Vt = 25
        gm = []
        for i in range(len(Ic)):
            gm.append(round(Ic[i] *1000/ Vt))

        plt.plot(Ic, gm, 'o-', label='gm vs $I_c$')

        for x,y in zip(Ic,gm):
            plt.text(x +0.2, y + 2, str(y) + "$m\\frac{A}{v}$")
            
        plt.ylim(min(gm) - 10 ,max(gm) + 10)    
        plt.xlabel('$I_c$ [mA]')
        plt.ylabel('gm [mA/V]')
        plt.title("gm vs $I_c$ ")
        plt.legend()
        grafica = 'g/grafica_4' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

              
        
        # --- Grafica 5: r_pi vs Ic --------
        plt.figure(5)
        r_pi = []
        for i in range(len(Ic)):
            r_pi.append(round((Beta[i]*1000/gm[i]) ))
        plt.plot(Ic, r_pi, 'o-', label= '$r_\\pi$ vs $I_c$')
        for x,y in zip(Ic,r_pi):
            plt.text(x +0.1, y, str(y) + "$\\Omega$")
            
        plt.xlabel('$I_c$ [mA]')
        plt.ylabel('$r_\\pi [\\Omega]$')
        plt.title("$r_\\pi$ vs $I_c$")
        plt.legend()
        grafica = 'g/grafica_5' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)

        # --- Grafica 6: r_0 vs Ic ----------
        #########################################################################################################
        # -- OBTENCION DE PENDIENTE
        m = [] # pendiente de la recta
        num =[] # numerador para calcular m
        den =[] # denominador para calcular m        
        
        b = []# abscisa, de la forma  y = Vax + b
        Va=[]
        
        for i in range(len(muestras['Ic_lp'])-1):
            num.append(round(muestras['Ic_lp'][i][1] - muestras['Ic_lp'][i][3], 3))
            den.append(round(muestras['Vce_lp'][i][1] - muestras['Vce_lp'][i][3], 3))
            m.append(round(num[i]/den[i], 3))
            if (m[i] == 0) or (m[i] < 0.02) :
                m[i] = 0.023 # en caso de la pendiente sea 0, se hace una suposición, asignado un valor pequeño
            if m[i]<0:                
                m[i] = -1* m[i]
            b.append(round(-m[i] * muestras['Vce_lp'][i][3] + muestras['Ic_lp'][i][3], 3))
            Va.append(round(-b[i]/ m[i]))
            
        Va_promedio = round(np.average(Va)) # valor promedio del arreglo de Va

        #depuracion de los valores para obtener Va. Va = -b/m, ya que la amplitud  = 0, intersección con eje horizontal
        #####RESUMEN DE DATOS DEL TRANSISTOR#################################
        print("*****RESUMEN DE LOS DATOS DEL TRANSISTOR BJT********")
        print("Valores de corriente I_c [mA] (5 curvas): ", Ic)
        print("Valores de corriente I_b [uA] (5 curvas): ", Ib)
        print("Voltaje de encendido V_beON [V]: " + label_VbeON )
        print("Valor de pendiente: ", m)
        print("Valor de abscisa: ", b)
        print("Valor de Va [V]: ", Va)
        print("Valor de Va promedio [V]: ", Va_promedio)
        print("Beta promedio:", Beta_promedio)
        
        for i in range(len(muestras['Ic'][0])):
            if muestras['Ic_lp'][0][i] == 0:
                print("Voltaje de saturacion: "+  str(muestras['Vce_lp'][0][i-1]) + " V")
                break
        
        ########################################################################
        
        plt.figure(6)
        r_0=[]
        for i in range(len(Ic)):
            r_0.append(round(-Va_promedio/Ic[i])) 
        plt.plot(Ic, r_0, 'o-', label='$r_0$ vs Ic, ' + '$V_a$ = ' + str(Va_promedio) + " V")
        for x,y in zip(Ic,gm):
            plt.text(x +0.2, y + 2, str(y) + "$K\\Omega$")
        for x,y in zip(Ic,r_0):
            plt.text(x +0.1, y, str(y) + "$ K\\Omega$")
        plt.xlabel('$I_c$ [mA]')
        plt.ylabel('$r_0$ [K$\\Omega]$')
        plt.title("$r_0$ vs $I_c$")
        plt.legend()
        grafica = 'g/grafica_6' + ".jpg"
        plt.savefig(grafica)
        graficas.append(grafica)
        #########################################################################################################################

        # --- Grafica 7: Ic vs Vce [PROMEDIADO - LowPass] ---
        plt.figure(7)
        diagrama = img.imread('i/ArduinoUno_Esquematico.jpg')
        plt.imshow(diagrama)
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

            

         
