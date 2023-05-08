import cv2
import math
import time
import numpy as np
import mediapipe as mp
from random import random


sets=input("Enter number of sets ")


up = False
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
x_axis_label = 'Time'
y_axis_label = 'Angle '


angles=np.zeros((500,))
angle=0
index=0
counter=0
reps=0
start_time =0
countdown = 15
br=False

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
            up = True
            counter += 1
        elif points[14][1] > points[12][1]:
            up = False

    except:
        pass

    # cv2.putText(image, str(counter), (100,150),cv2.FONT_HERSHEY_PLAIN, 12, (255,0,0),12) #Old already existed
    
    #******************* Statistics *****************
    # print(angle)
    angles[index]=angle

    cv2.line(image, (50, 650), (650, 650), (255, 255, 255), 2) #horizontal
    cv2.line(image, (50, 650), (50, 250), (255, 255, 255), 2)   #vertical

    for i in range(1, index + 1):
        x1 = 50 + (i - 1) * 400 // 300
        y1 = 650 - int(angles[i - 1] * 4.0 / 1000.0 * 400)
        x2 = 50 + i * 400 // 300
        y2 = 650 - int(angles[i] * 4.0 / 1000.0 * 400)

        # print(y1)
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.putText(image, x_axis_label, (30 + 500 // 2 - 30, 50 + 600 + 30), font, font_scale, (0,0,0), 2, cv2.LINE_AA)
    cv2.putText(image, y_axis_label, (45 - 40, 50 + 600 // 2), font, font_scale, (0,0,0), 2, cv2.LINE_AA)

    cv2.rectangle(image, (0,0), (100,73), (245,117,16), -1)
    cv2.rectangle(image, (1120,0), (1300,73), (245,117,16), -1)

    #******************* programming logic for counting break and reps *****************
    av=0
    for i in range(0,80):
        av+=angles[index-i]
    av/=20.0

    if(av>=8 and av<=15 and counter>0):
        br=True

    # Counting break 
    if br and start_time==0:
        start_time=time.time()
        reps=counter

        countdown=15
        sets=str(int(sets)-1)
        counter=0

    if(br):
        elapsed_time = time.time() - start_time
        remaining_time = max(countdown - elapsed_time, 0)
        remaining_seconds = int(remaining_time)

        if elapsed_time<3:
            pqr=""
            if(reps>7):
                pqr=str(reps) + " reps, Well Done! Increase your weight by 2.5"
                    
            elif(reps<5):
                pqr=str(reps) + " reps, Lighten up your equipment weight by 2.5"

            else:
                pqr=str(reps) + " reps, Badhiya jaa raha hai Guru"

            cv2.putText(image, pqr , (200,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,139), 3, cv2.LINE_AA)                

        else:
            countdown_str = f"Counting Break.. {remaining_seconds} seconds"
            cv2.putText(image, countdown_str, (200,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,139), 3, cv2.LINE_AA)


        if int(sets)==0:
            break;
            
        if counter>0:
            br=False
            start_time=0

        # *******************                    DONE                             *****************


    # Rep data
    cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(counter), (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
    
     # Sets data
    cv2.putText(image, 'SETS REMAINING', (1130,12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(sets), (1170,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

    cv2.imshow('Mediapipe Feed', image)
    index = (index + 1) % 300
    time.sleep(0.001)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()



