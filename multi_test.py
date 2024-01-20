#importacion de librerias
import numpy as np
import time
import subprocess
from pynput.keyboard import Controller
import cv2


#Se crea un objeto Controller para controlar el teclado.
keyboard = Controller()

# Configuración de pantalla completa y optimización
isfullscreen = "NO"
makefullscreen = isfullscreen == "SI"

isoptimized = "SI"
makeoptimize = isoptimized == "SI"

# Documentación de variables de configuración
"""
Variables de configuración:
- isfullscreen: Indica si la aplicación se ejecuta en modo de pantalla completa ("SI" o "NO").
- makefullscreen: Booleano que representa si la aplicación debe ejecutarse en modo de pantalla completa.
- isoptimized: Indica si se aplica la optimización ("SI" o "NO").
- makeoptimize: Booleano que representa si se deben aplicar optimizaciones.
"""

#declaracion del numero de zonas
total_zones = 11
touchcaps = []

zones_coordinates = [
    {"cap1": (7, 14), "cap2": (137, 110), "com": ["a"]},
    {"cap1": (178, 14), "cap2": (306, 110), "com": ["b"]},
    {"cap1": (344, 14), "cap2": (467, 110), "com": ["c"]},
    {"cap1": (507, 15), "cap2": (630, 102), "com": ["d"]},
    {"cap1": (8, 135), "cap2": (139, 234), "com": ["e"]},
    {"cap1": (244, 154), "cap2": (409, 230), "com": ["f"]},
    {"cap1": (507, 133), "cap2": (631, 209), "com": ["g"]},
    {"cap1": (10, 258), "cap2": (140, 358), "com": ["h"]},
    {"cap1": (182, 258), "cap2": (307, 358), "com": ["i"]},
    {"cap1": (348, 258), "cap2": (467, 358), "com": ["j"]},
    {"cap1": (507, 231), "cap2": (633, 358), "com": ["k"]}
]

# Inicialización de las zonas
for i, zone_data in enumerate(zones_coordinates):
    zone_data.update({"last": 0, "detected": False, "timer": 0})
    touchcaps.append(zone_data)
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

# Lista de desarrolladores
lista_desarrolladores = ["Dr. Gaspar.S.G","Miguel Angel C.V","Wlliam J.C.O"]

#obtiene los nombres de los scripts que se abren
scripts_abiertos = set() 

# guarda los nosmbres de los scrips para llamarlos posteriomente
# base nombre de los script
base_script_name = "hands_3d{}.py"

# Nombres de los scripts asociados a letras
# Se utiliza un diccionario de comprensión para generar automáticamente los nombres de los scripts
# desde 'a' hasta 'k', y luego se agrega 'k' con el mismo script que 'a'
# Nombres de los scripts
script_names = {chr(ord('a') + i): base_script_name.format(i + 1) for i in range(11)}

# Agregar 'k' con el mismo script que 'a'
script_names['k'] = base_script_name.format(11)

# Documentación
"""
Nombres de los scripts asociados a letras:

Variables:
- base_script_name: La parte común del nombre de los scripts.
- script_names: Diccionario que asocia letras ('a'-'k') con nombres de scripts correspondientes.

Estructura del diccionario script_names:
- Clave: Letra asociada al script ('a'-'k').
- Valor: Nombre del script correspondiente.

Ejemplo de script_names:
{
    "a": "hands _3d1.py",
    "b": "hands _3d2.py",
    ...
    "k": "hands _3d1.py"  
}
"""
barra = "barra_carga.py"


# Variable para checar si el script externo ya está abierto
script_abierto = False

# Variable para almacenar el nombre del script actualmente ejecutándose
script_actual = None

# Variable que almacena el proceso del script externo (la instancia Popen)
script_proceso = None  

# Variable para almacenar el último tiempo en que se intentó abrir el script
# Variable para almacenar el último tiempo de apertura
ultimo_tiempo_apertura = 0 

# Variable para almacenar el último tiempo de apertura exitosa del script
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
counter = 0        # Contador de gestos o movimientos
lastgestureX = 0   # Última posición X del gesto
lastgestureY = 0   # Última posición Y del gesto
lastgestureZ = 0   # Última posición Z del gesto
moveDelta = 30     # Umbral de cambio para considerar un movimiento
lastmoveX = 0      # Última posición X del movimiento
lastmoveY = 0      # Última posición Y del movimiento
lastmoveZ = 0      # Última posición Z del movimiento
waitframe = True   # Indicador de espera de cuadro
moveX = 0          # Posición X del movimiento actual
moveY = 0          # Posición Y del movimiento actual
moveZ = 0          # Posición Z del movimiento actual
newZ = True        # Indicador de nueva posición Z
refZ = 0           # Posición de referencia Z
absZ = 0           # Valor absoluto de la posición Z
initialpose = True # Indicador de la pose inicial
zoomcounter = 0    # Contador de zoom


"""
    Cierra el script asociado a la barra de progreso si la mano se retira de ciertas zonas.
    """
def cerrar_contador():
    global script_abierto, script_actual, script_proceso, ultimo_tiempo_apertura

    try:
         # Verifica si el script actual es el de la barra y está abierto
        if script_actual == barra and script_abierto:
                cerrar_script_externo()  # Cierra el script actual
    except Exception as e:
        print("Error al cerrar el script del contador:", e)
#funcion para calcular la distancia netre dos puntos
def calc_distance(p1, p2):
    return sqrt((p1[0]-p2[0])*2+(p1[1]-p2[1])*2)
#funcion para 


    """
    Abre un script externo asociado a una letra, cerrando el script actual si es necesario.

    Parameters:
    - letra (str): La letra asociada al script que se va a abrir.
    """
def abrir_script_externo(letra):
    global script_abierto, script_actual, script_proceso, ultimo_tiempo_apertura

    try:
        # Cierra el script actual si es diferente del actual
        if script_actual :
            print(f"Ya hay un script abierto: {script_actual}")
            # en revision  esto se puso porque se cerraba y se abria el script actual
            #cierra el script actual solo si el script
            #abierto es diferente del actual
            if script_abierto != script_actual:
                cerrar_script_externo()
                
            # Verifica si ha pasado menos de 3 segundos desde la última apertura
            #tiempo_actual = time.time()
            if tiempo_actual - ultimo_tiempo_apertura < 3:
                print("Debe esperar 3 segundos antes de abrir otro script.")
                return

        # Sino hay scripts abiertos, entonces permite abrir uno
        script_name = script_names.get(letra, " ")
           # Verifica si el script `contador2.py` ya está abierto
        if script_name == barra and script_name in scripts_abiertos:
              print(f"El script {barra} ya está abierto.")
              return
        
        
        # Permite abrir otro script
        if script_name:
            script_proceso = subprocess.Popen(["python", script_name])
            scripts_abiertos.add(script_name)
            script_abierto = True
            script_actual = script_name
        else:
                print(f"No se encontró el script para la letra '{letra}'")

    except Exception as e:
        print("Error al abrir el script externo:", e)


    """
    Cierra el script externo actual si está abierto.
    """
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

hand_inside_region = False

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1) as hands:
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


        credit_text = f"Desarrollado por: {', '.join(lista_desarrolladores)}"
        cv2.putText(image, credit_text, (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1, cv2.LINE_AA)
        if not makefullscreen:
            cv2.imshow('Hand Tracking', image)

          
        # Salir del bucle si se presiona la tecla 'esc'
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
#se cambio la condicion para que no se cierre el script
#actual si dejas la  mano sobre la zona
if script_abierto:
    cerrar_script_externo()

cap.release()
cv2.destroyAllWindows()
