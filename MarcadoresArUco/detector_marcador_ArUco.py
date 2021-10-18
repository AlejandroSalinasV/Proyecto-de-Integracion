#******************************************************
#
#  DETECCION DE MARCADORES ArUco sobre una Protoboard
#
#  Se emplean 15 marcadores ArUco tipo "DICT_4X4_50" impresos
#  al 10% de su tamaño original, con los siguientes ID:
#  10, 11, 12, 13, 14, 15, 16, 17 ,18, 19, 20, 21, 22, 23  y 24,
#  todos ellos colocados aleatoriamente y en cualquier orientación
#  sobre la protoboard en conjunto con los componentes y fuera de
#  ésta.
#
#  Programa adaptado de:
#
#  https://www.pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/
#
#                                   2 / febrero / 2021
#
#******************************************************

# import the necessary packages
import argparse
import imutils
import cv2
import sys

# --- Del diccionario completo de marcadores ArUco, sólo se
#     utiliza el tipo: "DICT_4X4_50" 
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50
}

# --- Proto con marcadores a 10% de su tamaño con marco ---
image = cv2.imread("circuitod6.jpg")

# --- Sin importar el tamaño de la imagen, se escala a width = 600 ---
image = imutils.resize(image, width=1000)

# --- Detección de los marcadores ArUco ---
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_50"])
 
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
	parameters=arucoParams)
### detectMarkers (imagen, diccionario, parametros)
### Regresa, corners, ids, rejected (marcadores rechazados)


# --- Verficica que al menos se detectó un marcador ArUco ---
print("Se detectaron: ",len(corners)," marcadores ArUco")
print(corners)
if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
                # extract the marker corners (which are always returned in
                # top-left, top-right, bottom-right, and bottom-left order)
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                # draw the bounding box of the ArUCo detection
                cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(image, topRight, bottomRight, (255, 255, 0), 2)
                cv2.line(image, bottomRight, bottomLeft, (255, 0, 0), 2)
                cv2.line(image, bottomLeft, topLeft, (0, 255, 255), 2)
                # compute and draw the center (x, y)-coordinates of the ArUco
                # marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                # draw the ArUco marker ID on the image
                cv2.putText(image, str(markerID),
                        (cX+10, cY + 15 ), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
                print("[INFO] Marcador ArUco ID: {}".format(markerID))
                # show the output image
                cv2.imshow("Circuito Bajo Prueba", image)
                cv2.waitKey(0)
