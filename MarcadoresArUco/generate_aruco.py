#******************************************************
#
#  GENERACION DE MARCADORES ArUco 
#  
#  - Se determino generar los marcadores mas sencillos (4x4),
#    los cuales, de acuerdo al diccionario ArUco, tienen la
#    capacidad de generar hasta 50 marcadores diferentes (4x4_50).
#    Para este proyecto, esa cantidad es suficiente.
#    En este programa se generan los marcadores (4x4_50) con los
#    siguientes identificadores (ID): (15 marcadores en total)
#    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 y 24
#
#                                   30 / enero / 2021
#
#  REFERENCIA:
# ttps://www.pyimagesearch.com/2020/12/14/generating-aruco-markers-with-opencv-and-python/
#
#******************************************************

# import the necessary packages
import numpy as np
import argparse
import cv2
import sys

# ------------------------------------------------------
# Aqui se define:
# Tipo de marcador: "DICT_4X4_50"
# Identificador: "id" de acuerdo al que se elija
# Nombre del archivo (imagen) que se guarda en disco:
#                       marcador
# ------------------------------------------------------
tipo = "DICT_4X4_50"
identificador = 10
marcador = "DICT_4X4_50_id10.jpg"

# ------------------------------------------------------
#                DICCIONARIO ArUco
# ------------------------------------------------------
# Define los nombres de cada posible marcador ArUco que
#               pueda manejar OpenCV
# ------------------------------------------------------
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

# ---------------------------------------------------------------
# Verifica que exista el marcador ArUco proporcionado y que lo
#                       pueda manejar OpenCV
# ---------------------------------------------------------------
if ARUCO_DICT.get("DICT_5X5_100", None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(
		tipo))
        sys.exit(0)

# ---------------------------------------------------------------
#               Carga el diccionario de ArUco
# ---------------------------------------------------------------
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[tipo])

# ---------------------------------------------------------------
# Crea un espacio de memoria para colocar el marcador ArUco que
#  se va a generar y lo "dibuja" en dicho espacio de memoria
# ---------------------------------------------------------------
print("[INFO] generando el marcador ArUCo tipo '{}' con ID '{}'".format(
	tipo, identificador))
tag = np.zeros((300, 300, 1), dtype="uint8")
cv2.aruco.drawMarker(arucoDict, identificador, 300, tag, 1)

# ---------------------------------------------------------------
#   Escribe (guarda) en disco, el marcador ArUco generado y lo
#                  despliega en pantalla
# ---------------------------------------------------------------
cv2.imwrite(marcador, tag)
cv2.imshow("Marcador ArUCo", tag)
cv2.waitKey(0)
