import cv2
import math
import time
import numpy as np
import mediapipe as mp
from random import random

angles=np.zeros((500,))
angle=0
index=0
up = False
counter = 0

# ******************** rep ************************

mp_drawing = mp.solutions.drawing_utils
mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
cap = cv2.VideoCapture(0)

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

while cap.isOpened():
    # success, img = cap.read()
    # img = cv2.resize(img, (1280,720))

    ret, frame = cap.read()

    # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
      
    # Make detection
    results = pose.process(image)

    # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # if results.pose_landmarks:
    try:
        landmarks = results.pose_landmarks.landmark
        mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)


        #get coordinates for angles in graph
        hip= [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

        # Calculate angle
        angle = calculate_angle(hip, shoulder, elbow)
        
        points = {}
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = image.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            # print(id,lm,cx,cy)
            points[id] = (cx,cy)

        cv2.circle(image, points[12], 15, (255,0,0), cv2.FILLED)
        cv2.circle(image, points[14], 15, (255,0,0), cv2.FILLED)
        cv2.circle(image, points[11], 15, (255,0,0), cv2.FILLED)
        cv2.circle(image, points[13], 15, (255,0,0), cv2.FILLED)


        if not up and points[14][1] + 40 < points[12][1]:
            print("UP")
            up = True
            counter += 1
        elif points[14][1] > points[12][1]:
            print("Down")
            up = False

    except:
        pass

    cv2.putText(image, str(counter), (100,150),cv2.FONT_HERSHEY_PLAIN, 12, (255,0,0),12) #Old already existed
    #Statistics 
    
    angles[index]=angle

    cv2.line(image, (50, 450), (450, 450), (255, 255, 255), 2) #horizontal
    cv2.line(image, (50, 450), (50, 50), (255, 255, 255), 2)   #vertical

    for i in range(1, index + 1):
        x1 = 50 + (i - 1) * 400 // 500
        y1 = 450 - int(angles[i - 1] * 4.0 / 1000.0 * 400)
        x2 = 50 + i * 400 // 500
        y2 = 450 - int(angles[i] * 4.0 / 1000.0 * 400)

        # print(y1)
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)


    cv2.imshow('Mediapipe Feed', image)
    index = (index + 1) % 500
    time.sleep(0.001)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()



