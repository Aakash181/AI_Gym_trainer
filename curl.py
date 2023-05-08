import cv2
import math
import time
import numpy as np
import mediapipe as mp
from random import random

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
font_color = (255, 255, 255)
x_axis_label = 'Time'
y_axis_label = 'Angle '

sets=input("Enter number of sets ")
# weight=input("Enter weight of dumbell/barbell ")

# ******************** curl ************************

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# global variables
angles=np.zeros((500,))
angle=0
index=0
counter=0
reps=0
start_time =0
countdown = 15
br=False
br_check=False



def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 
# Curl counter variables
stage = None


## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
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
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)
            
            # Visualize angle
            cv2.putText(image, str(angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            # Curl counter logic
            if angle > 160:
                stage = "down"
            if angle < 30 and stage =='down':
                stage="up"
                counter +=1
                # print(counter)
                       
        except:
            pass


        #******************* Statistics *****************
        angles[index]=angle

        cv2.line(image, (50, 650), (650, 650), (255, 255, 255), 2) #horizontal
        cv2.line(image, (50, 650), (50, 250), (255, 255, 255), 2)   #vertical

        for i in range(1, index + 1):
            x1 = 50 + (i - 1) * 400 // 300
            y1 = 650 - int(angles[i - 1] * 4.0 / 1000.0 * 300)

            x2 = 50 + i * 400 // 300
            y2 = 650 - int(angles[i] * 4.0 / 1000.0 * 300)

            # print(y1)
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

            
            
        cv2.putText(image, x_axis_label, (30 + 500 // 2 - 30, 50 + 600 + 30), font, font_scale, font_color, 1, cv2.LINE_AA)
        cv2.putText(image, y_axis_label, (59 - 40, 50 + 600 // 2), font, font_scale, font_color, 1, cv2.LINE_AA)
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        cv2.rectangle(image, (1120,0), (1300,73), (245,117,16), -1)

        #******************* programming logic for counting break and reps *****************
        av=0
        for i in range(0,20):
            av+=angles[index-i]
        av/=20.0

        if(av>=165 and av<=180 and counter>0):
            br=True

        # Counting break 
        if br and start_time==0:
            start_time=time.time()
            reps=counter

            countdown=15
            sets=str(int(sets)-1)
            counter=0

        if(br):
            # print("Hello")
            elapsed_time = time.time() - start_time
            remaining_time = max(countdown - elapsed_time, 0)
            remaining_seconds = int(remaining_time)

            if elapsed_time<3:
                pqr=""
                if(reps>12):
                    pqr=str(reps) + " reps, Well Done! Increase your weight by 2.5"
                    
                elif(reps<8):
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
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Sets data
        cv2.putText(image, 'SETS REMAINING', (1130,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(sets), 
                    (1170,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)
        index = (index + 1) % 300
        time.sleep(0.001)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    

    cap.release()
    cv2.destroyAllWindows()