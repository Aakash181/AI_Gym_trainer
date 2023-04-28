import cv2
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture(0)
up = False
counter = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280,720))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    # print("-----------------------------------------------------")
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        points = {}
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            # print(id,lm,cx,cy)
            points[id] = (cx,cy)


        cv2.circle(img, points[12], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[14], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[11], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[13], 15, (255,0,0), cv2.FILLED)


        if not up and points[14][1] + 40 < points[12][1]:
            print("UP")
            up = True
            counter += 1
        elif points[14][1] > points[12][1]:
            print("Down")
            up = False
        # print("----------------------",counter)

    cv2.putText(img, str(counter), (100,150),cv2.FONT_HERSHEY_PLAIN, 12, (255,0,0),12)










    cv2.imshow("img",img)
    cv2.waitKey(1)




