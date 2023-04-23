import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm


file_name = 'bench_press.mp4'

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"


while cap.isOpened():
    ret, img = cap.read() #640 x 480
    #Determine dimensions of video - Help with creation of box in Line 43
    width  = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        left_elbow = detector.findAngle(img, 11, 13, 15)
        left_shoulder = detector.findAngle(img, 13, 11, 23)
        left_hip = detector.findAngle(img, 11, 23, 25)
        
        right_elbow = detector.findAngle(img, 12, 14, 16)
        right_shoulder = detector.findAngle(img, 14, 12, 24)
        right_hip = detector.findAngle(img, 12, 24, 26)
        
        #Percentage of success of bench press
        left_per = np.interp(left_elbow, (80, 160), (0, 100))
        right_per = np.interp(right_elbow, (80, 160), (0, 100))
        
        #Bar to show bench press progress for left and right hands
        left_bar = np.interp(left_elbow, (80, 160), (380, 50))
        right_bar = np.interp(right_elbow, (80, 160), (380, 50))

        #Check to ensure right form before starting the program
        if left_elbow > 160 and left_shoulder > 40 and left_hip > 160 and right_elbow > 160 and right_shoulder > 40 and right_hip > 160:
            form = 1
    
        #Check for full range of motion for the bench press
        if form == 1:
            if left_per == 0 and right_per == 0:
                if left_elbow <= 80 and left_hip > 160 and right_elbow <= 80 and right_hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 1
                        direction = 1
                else:
                    feedback = "Fix Form"
                    
            if left_per == 100 and right_per == 100:
                if left_elbow > 160 and left_shoulder > 40 and left_hip > 160 and right_elbow > 160 and right_shoulder > 40 and right_hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 1
                        direction = 0
                else:
                    feedback = "Fix Form"
                        # form = 0
                
                    
    
        print(count)
        
        #Draw Bars
        if form == 1:
            # Left bar
            left_bar_start = (100, 200)
            left_bar_end = (120, 50)
            cv2.rectangle(img, left_bar_start, left_bar_end, (0, 255, 0), 3)
            left_bar_height = np.interp(lmList[13][2], (left_bar_start[1], left_bar_end[1]), (0, 100))
            left_bar_y = np.interp(left_bar_height, (0, 100), (left_bar_end[1], left_bar_start[1]))
            cv2.rectangle(img, (left_bar_start[0], int(left_bar_y)), (left_bar_end[0], left_bar_start[1]), (0, 255, 0), cv2.FILLED)
            
            # Right bar
            right_bar_start = (width-100, 200)
            right_bar_end = (width-120, 50)
            cv2.rectangle(img, right_bar_start, right_bar_end, (0, 255, 0), 3)
            right_bar_height = np.interp(lmList[14][2], (right_bar_start[1], right_bar_end[1]), (0, 100))
            right_bar_y = np.interp(right_bar_height, (0, 100), (right_bar_end[1], right_bar_start[1]))
            cv2.rectangle(img, (right_bar_start[0], int(right_bar_y)), (right_bar_end[0], right_bar_start[1]), (0, 255, 0), cv2.FILLED)

        #bench_press counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        
        #Feedback 
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

    # Show the video output in a window
    cv2.namedWindow('Pushup counter', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Pushup counter', 1000, 800)    
    cv2.imshow('Pushup counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()