#v10
#importacion de librerias
import numpy as np
import time
import subprocess
from pynput.keyboard import Controller

#Se crea un objeto Controller para controlar el teclado.
keyboard = Controller()

# configuracion de ventana
"""
Variables de configuración:
- isfullscreen: Indica si la aplicación se ejecuta en modo de pantalla completa ("SI" o "NO").
- makefullscreen: Booleano que representa si la aplicación debe ejecutarse en modo de pantalla completa.
- isoptimized: Indica si se aplica la optimización ("SI" o "NO").
- makeoptimize: Booleano que representa si se deben aplicar optimizaciones.
"""

isfullscreen = "NO"
makefullscreen = isfullscreen == "SI"
isoptimized = "SI"
makeoptimize = isoptimized == "SI" 

# Documentación
"""
Declaración del número de zonas y definición de las coordenadas de las figuras (ventanas).

Variables:
- total_zones: Número total de zonas.
- touchcaps: Lista que almacenará información sobre cada zona.

Estructura de cada zona (diccionario en touchcaps):
- cap1: Coordenada del vértice superior izquierdo.
- cap2: Coordenada del vértice inferior derecho.
- com: Lista de comandos asociados a la zona.
- last: Último índice utilizado en la lista de comandos.
- detected: Indica si la mano ha sido detectada en la zona.
- timer: Tiempo transcurrido desde la última detección.
"""
#declaracion del numero de zonas
total_zones= int(11)
touchcaps = []

#zona de coordenadas de las figuras (ventanas)
zones_data = [
    {"cap1": (7, 14), "cap2": (137, 110), "com": ["a"],"last": 0},
    {"cap1": (178, 14), "cap2": (306, 110), "com": ["b"],"last": 0},
    {"cap1": (344, 14), "cap2": (467, 110), "com": ["c"],"last": 0},
    {"cap1": (507, 15), "cap2": (630, 102), "com": ["d"],"last": 0},
    {"cap1": (8, 135), "cap2": (139, 234), "com": ["e"],"last": 0},
    {"cap1": (244, 154), "cap2": (409, 230), "com": ["f"],"last": 0},
    {"cap1": (507, 133), "cap2": (631, 209), "com": ["g"],"last": 0},
    {"cap1": (10, 258), "cap2": (140, 358), "com": ["h"],"last": 0},
    {"cap1": (182, 258), "cap2": (307, 358), "com": ["i"],"last": 0},
    {"cap1": (348, 258), "cap2": (467, 358), "com": ["j"],"last": 0},
    {"cap1": (507, 231), "cap2": (633, 358), "com": ["k"],"last": 0}
]
# Inicialización de las zonas
for zone in zones_data:
    zone["detected"] = False  # Inicializa "detected" en False
    zone["timer"] = 0  # Inicializa "timer" en 0

# Añadir las zonas inicializadas a touchcaps
touchcaps.extend(zones_data)


scripts_abiertos = set() #obtiene los nombres de los scripts que se abren

# guarda los nosmbres de los scrips para llamarlos posteriomente
script_names = {
    
    "a": "hands_3d_final1.py",
    "b": "hands_3d_final2.py",
    "c": "hands_3d_final3.py",
    "d": "hands_3d_final4.py",
    "e": "hands_3d_final5.py",
    "f": "hands_3d_final6.py",
    "g": "hands_3d_final7.py",
    "h": "hands_3d_final8.py",
    "i": "hands_3d_final9.py",
    "j": "hands_3d_final10.py",
    "k": "hands_3d_final11.py",
    
    }
barra = "contador2.py"
aviso = "aviso.py"
# Variable para checar si el script externo ya está abierto
script_abierto = False
script_actual = None
script_proceso = None  
ultimo_tiempo_apertura = 0 # Variable para almacenar el último tiempo de apertura
ultimo_tiempo_apertura_exitosa = 0


################ segundo codigo ########################################
print("Ejecutando...")

import mediapipe as mp 
import cv2
import numpy as np
from math import sqrt
import signal

"""
    estas líneas crean alias para módulos 
    específicos dentro de la biblioteca MediaPipe,
    lo que hace que sea más conveniente utilizar las 
    utilidades de seguimiento de manos y dibujo en el código
        
"""
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#en esta parte se elige el indice de la camara (por si hay una camara externa)
if makeoptimize:
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(0)

"""
estas líneas de código están 
ajustando la resolución de los 
fotogramas de video capturados  
"""
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

"""
   este bloque de código se encarga 
   de la gestión de variables relacionadas
   con el seguimiento de gestos y la 
   interacción con las zonas de control 
   en el programa.
"""
counter = 0 
lastgestureX = 0
lastgestureY = 0
lastgestureZ = 0
moveDelta = 30
lastmoveX = 0
lastmoveY = 0
lastmoveZ = 0
waitframe = True
moveX = 0
moveY = 0
moveZ = 0
newZ = True
refZ = 0
absZ = 0
initialpose = True
zoomcounter = 0
#funcion para cerra la barra de progreso por si la mano se quita de 
#las zonas
def cerrar_contador():
    global script_abierto, script_actual, script_proceso, ultimo_tiempo_apertura

    try:
        if script_actual == barra and script_abierto:
                cerrar_script_externo()
                script_proceso = subprocess.Popen(["python", aviso])
    except Exception as e:
        print("Error al cerrar el script del contador:", e)


#funcion para calcular la distancia netre dos puntos
def calc_distance(p1, p2):
    return sqrt((p1[0]-p2[0])*2+(p1[1]-p2[1])*2)
#funcion para 
###############################################################
def abrir_script_externo(letra):
    global script_abierto, script_actual, script_proceso, ultimo_tiempo_apertura

    try:
        # Verificar si hay un script abierto y manejar la situación
        if script_actual:
            print(f"Ya hay un script abierto: {script_actual}")
            cerrar_script_externo()
            
            # Si ha pasado menos de 3 segundos desde la última apertura, no permite abrir otro script
            tiempo_actual = time.time()
            if tiempo_actual - ultimo_tiempo_apertura < 3:
                print("Debe esperar 3 segundos antes de abrir otro script.")
                return

        # Obtener el nombre del script correspondiente a la letra
        script_name = script_names.get(letra, "")
        
        # Verificar si el script ya está abierto y manejar la situación
        if script_name == barra and script_name in scripts_abiertos:
            print(f"El script {barra} ya está abierto.")
            return

        # Abrir un nuevo script
        if script_name:
            cerrar_script_externo()  # Cerrar cualquier script abierto antes de abrir uno nuevo
            script_proceso = subprocess.Popen(["python", script_name])
            scripts_abiertos.add(script_name)
            script_abierto = True
            script_actual = script_name
            ultimo_tiempo_apertura = time.time()
        else:
            print(f"No se encontró el script para la letra '{letra}'")
    except Exception as e:
        print("Error al abrir el script externo:", e)


def cerrar_script_externo():
    global script_abierto, script_actual, script_proceso
    try:
        if script_abierto:
            if script_proceso:
                script_proceso.send_signal(signal.SIGTERM)
                script_proceso.wait()
                script_proceso = None
            script_abierto = False
            script_actual = None
        else:
            print("No hay ningún script abierto")
    except Exception as e:
        print("Error al cerrar el script externo:", e)
###########################################################

hand_inside_region = False

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():

        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frameWidth = image.shape[1]
        frameHeight = image.shape[0]

        image = cv2.flip(image, 1)

        image.flags.writeable = False

        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        pos = (0, 0)
        cv2.rectangle(image, pos, (frameWidth, frameHeight), (0, 0, 0), -1)

        hands_inside_regions = [False] * len(touchcaps)

        totalHands = 0

        if results.multi_handedness:
            totalHands = len(results.multi_handedness)
            if totalHands == 2:
                if results.multi_handedness[0].classification[0].label == results.multi_handedness[1].classification[0].label:
                    totalHands = 1

        if results.multi_hand_landmarks:
            if initialpose:
                initialpose = False
                
            hand = results.multi_hand_landmarks[0]
            if totalHands == 1:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    indexTip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    indexTipXY = mp_drawing._normalized_to_pixel_coordinates(indexTip.x, indexTip.y, frameWidth, frameHeight)

                    thumbTip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP]
                    thumbTipXY = mp_drawing._normalized_to_pixel_coordinates(thumbTip.x, thumbTip.y, frameWidth, frameHeight)

                    if indexTipXY and thumbTipXY is not None:
                        indexXY = (indexTipXY[0], indexTipXY[1])
                        thumbXY = (thumbTipXY[0], thumbTipXY[1])
#en este ciclo principal se agrego el temporizador para que el script 
# sea llamado o se ejecute despues de mantener la mano por 5 segundos en la zona de gestos
                        for i, r in enumerate(touchcaps):
                            if r["cap1"][0] < indexXY[0] < r["cap2"][0] and r["cap1"][1] < indexXY[1] < r["cap2"][1]:
                                if not r["detected"]:
                                    r["detected"] = True
                                    tiempo_actual = time.time()
                                    tiempo_transcurrido_desde_ultima_apertura = tiempo_actual - ultimo_tiempo_apertura_exitosa
                                    # Verificar si el script de la barra de progreso no está abierto
                                    if not script_abierto or script_actual != barra or tiempo_transcurrido_desde_ultima_apertura >= 5:
                                          
                                            script_proceso = subprocess.Popen(["python", barra])
                                            #cerrar_script_externo()
                                            scripts_abiertos.add(barra)
                                            script_abierto = True
                                            script_actual = barra
                                            ultimo_tiempo_apertura_exitosa = tiempo_actual
                                    r["timer"] = time.time()  # Iniciar el temporizador
                                             
                                  
                                else:
                                    elapsed_time = time.time() - r["timer"]
                                    if elapsed_time >= 5:  # Si han pasado 5 segundos
                                        lastcom = r["last"]
                                        command = r["com"][lastcom]
                                        r["last"] = r["last"] + 1
                                        if r["last"] >= len(r["com"]):
                                            r["last"] = 0
                                           

                                        if command in script_names:
                                            abrir_script_externo(command)


                                        print(command)
                                        keyboard.press(command)
                                        time.sleep(0.1)
                                        keyboard.release(command)

                                hands_inside_regions[i] = True

                        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))

            elif totalHands == 2:
                handX = [0, 0]
                handY = [0, 0]
                isHands = [False, False]
                
                for num, hand in enumerate(results.multi_hand_landmarks):
                    indexTip = results.multi_hand_landmarks[num].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    indexTipXY = mp_drawing._normalized_to_pixel_coordinates(indexTip.x, indexTip.y, frameWidth, frameHeight)

                    thumbTip = results.multi_hand_landmarks[num].landmark[mp_hands.HandLandmark.THUMB_TIP]
                    thumbTipXY = mp_drawing._normalized_to_pixel_coordinates(thumbTip.x, thumbTip.y, frameWidth, frameHeight)

                    if indexTipXY and thumbTipXY is not None:
                        indexXY = (indexTipXY[0], indexXY[1])
                        thumbXY = (thumbTipXY[0], indexTipXY[1])

                        for i, r in enumerate(touchcaps):
                            if r["cap1"][0] < indexXY[0] < r["cap2"][0] and r["cap1"][1] < indexXY[1] < r["cap2"][1]:
                                if not r["detected"]:
                                    r["detected"] = True
                                    r["timer"] = time.time()  # Iniciar el temporizador
                                else:
                                    elapsed_time = time.time() - r["timer"]
                                    if elapsed_time >= 5:  # Si han pasado 5 segundos
                                        lastcom = r["last"]
                                        command = r["com"][lastcom]
                                        r["last"] = r["last"] + 1
                                        if r["last"] >= len(r["com"]):
                                            r["last"] = 0

                                        if command in script_names :
                                            abrir_script_externo(command)

                                        print(command)
                                        keyboard.press(command)
                                        time.sleep(0.1)
                                        keyboard.release(command)

                                hands_inside_regions[i] = True

                        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                            mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                        )

        else:
            if not initialpose:
                initialpose = True
                print("Posición inicial (MACV)")

        hand_inside_region = any(hands_inside_regions)

        if not hand_inside_region:
            cerrar_contador()
            for r in touchcaps:
                r["detected"] = False

        for r in touchcaps:
            cv2.rectangle(image, r["cap1"], r["cap2"], (255, 255, 255), 1)

        if not makefullscreen:
            # cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)
             #cv2.setWindowTitle('Hand Tracking', '')
             #cv2.setWindowProperty('Hand Tracking', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
             #cv2.setWindowProperty('Hand Tracking', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow('Hand Tracking', image)
           

        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
#se cambio la condicion para que no se cierre el script
#actual si dejas la  mano sobre la zona
if script_abierto:
    cerrar_script_externo()

cap.release()
cv2.destroyAllWindows()
