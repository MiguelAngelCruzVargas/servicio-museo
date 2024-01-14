import numpy as np
import open3d as o3d
import time
import threading
import mediapipe as mp
import cv2
import numpy as np
from math import sqrt
import uuid
import os
import tkinter as tk



# Inicializa el contador y el indicador de detección de manos
hand_detection_counter = 0
hands_detected = False


objectreadfile = "PIEZA6.obj"
isfullscreen = "NO"
makefullscreen = False
if isfullscreen == "SI":
    makefullscreen = True

isoptimized = "SI"
makeoptimize = False
if isoptimized == "SI":
    makeoptimize = True

mesh = o3d.io.read_triangle_mesh(objectreadfile, True)
mesh.compute_vertex_normals()
vis = o3d.visualization.Visualizer()
vis.create_window(width=1366//2, height=768)
if makefullscreen:
    vis.set_full_screen(True)    

vis.add_geometry(mesh)
vis.get_render_option().load_from_json("render_options.json")
vis.poll_events()
vis.update_renderer()

print("Ejecutando...")
import mediapipe as mp
import cv2
import numpy as np
from math import sqrt
import uuid
import os

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#camaras
if makeoptimize:
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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

def calc_distance(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) #calculando distancia

# ... (código anterior)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
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

        totalHands = 0

        if results.multi_handedness:
            totalHands = len(results.multi_handedness)
            if totalHands == 2:
                if (
                    results.multi_handedness[0].classification[0].label
                    == results.multi_handedness[1].classification[0].label
                ):
                    totalHands = 1

        if results.multi_hand_landmarks:
            if initialpose:
                initialpose = False

            for num, hand in enumerate(results.multi_hand_landmarks):
                normalized_landmarks = hand.landmark

                mp_drawing.draw_landmarks(
                    image,
                    hand,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                )

                # Modificación para usar todos los dedos
                handXY = [(int(point.x * frameWidth), int(point.y * frameHeight)) for point in hand.landmark]

                for finger_tip in handXY:
                    cv2.circle(image, finger_tip, 10, (255, 0, 0), 2)

                center = (
                    sum([handXY[mp_hands.HandLandmark.INDEX_FINGER_TIP][0], handXY[mp_hands.HandLandmark.MIDDLE_FINGER_TIP][0], handXY[mp_hands.HandLandmark.RING_FINGER_TIP][0], handXY[mp_hands.HandLandmark.PINKY_TIP][0]]) // 4,
                    sum([handXY[mp_hands.HandLandmark.INDEX_FINGER_TIP][1], handXY[mp_hands.HandLandmark.MIDDLE_FINGER_TIP][1], handXY[mp_hands.HandLandmark.RING_FINGER_TIP][1], handXY[mp_hands.HandLandmark.PINKY_TIP][1]]) // 4,
                )

                dist = calc_distance(handXY[mp_hands.HandLandmark.THUMB_TIP], center)
                if dist < 50:
                    netX = round((handXY[mp_hands.HandLandmark.THUMB_TIP][0] + center[0]) / 2)
                    netY = round((handXY[mp_hands.HandLandmark.THUMB_TIP][1] + center[1]) / 2)
                    cv2.circle(image, (netX, netY), 10, (0, 255, 0), 2)
                    deltaX = moveX - netX
                    moveX = netX
                    deltaY = moveY - netY
                    moveY = netY
                    if abs(deltaX) > 40 or abs(deltaY) > 40:
                        print("Max reached: " + str(deltaX) + "," + str(deltaY))
                    else:
                        print(str(deltaX) + "," + str(deltaY))
                        vis.get_view_control().rotate(-deltaX*10, -deltaY*10, xo=0.0, yo=0.0) #aqui se modifica la velocidad de la figura
                        vis.poll_events()
                        vis.update_renderer()
                else:
                    moveX = 0
                    moveY = 0

            if totalHands == 2:
                handX = [0, 0]
                handY = [0, 0]
                isHands = [False, False]

                for num, hand in enumerate(results.multi_hand_landmarks):
                    handXY = [(int(point.x * frameWidth), int(point.y * frameHeight)) for point in hand.landmark]

                    for finger_tip in handXY:
                        cv2.circle(image, finger_tip, 10, (255, 0, 0), 2)

                    center = (
                        sum([handXY[mp_hands.HandLandmark.INDEX_FINGER_TIP][0], handXY[mp_hands.HandLandmark.MIDDLE_FINGER_TIP][0], handXY[mp_hands.HandLandmark.RING_FINGER_TIP][0], handXY[mp_hands.HandLandmark.PINKY_TIP][0]]) // 4,
                        sum([handXY[mp_hands.HandLandmark.INDEX_FINGER_TIP][1], handXY[mp_hands.HandLandmark.MIDDLE_FINGER_TIP][1], handXY[mp_hands.HandLandmark.RING_FINGER_TIP][1], handXY[mp_hands.HandLandmark.PINKY_TIP][1]]) // 4,
                    )

                    dist = calc_distance(handXY[mp_hands.HandLandmark.THUMB_TIP], center)
                    if dist < 50:
                        netX = round((handXY[mp_hands.HandLandmark.THUMB_TIP][0] + center[0]) / 2)
                        netY = round((handXY[mp_hands.HandLandmark.THUMB_TIP][1] + center[1]) / 2)
                        handX[num] = netX
                        handY[num] = netY
                        isHands[num] = True

                if isHands[0] and isHands[1]:
                    distpar = calc_distance((handX[0], handY[0]), (handX[1], handY[1]))
                    if newZ:
                        newZ = False
                        moveZ = distpar
                        refZ = distpar
                    netX = round((handX[0] + handX[1]) / 2)
                    netY = round((handY[0] + handY[1]) / 2)
                    deltaZ = (distpar - moveZ) / refZ
                    if deltaZ < abs(1):
                        absZ = absZ - deltaZ
                        if absZ > 2.0:
                            absZ = 2.0
                        elif absZ < 0.5:
                            absZ = 0.5
                        moveZ = distpar
                        print(absZ)
                        cv2.circle(image, (netX, netY), 10, (0, 0, 255), 2)
                        vis.get_view_control().set_zoom(absZ)
                        vis.poll_events()
                        vis.update_renderer()

                elif not isHands[0] and not isHands[1]:
                    newZ = True

        else:
            if not initialpose:
                initialpose = True
                print("Regresando a posición Inicial")
                vis.get_view_control().set_zoom(1)

            vis.get_view_control().rotate(5, 0, xo=0.0, yo=0.0)
            zoomcounter = zoomcounter + 1
            if zoomcounter > 1000:
                zoomcounter = 0
            vis.poll_events()
            vis.update_renderer()

        if not makefullscreen:
            cv2.imshow("Hand Tracking", image)

        if results.multi_hand_landmarks:
            hands_detected = True
            hand_detection_counter = 0

        else:
            hand_detection_counter += 1

        if hand_detection_counter >= 50:
            print("No se ha detectado movimiento durante segundos. Cerrando el script.")
            break

        if cv2.waitKey(1) & 0xFF == ord(" "):
            break

cap.release()
cv2.destroyAllWindows()


