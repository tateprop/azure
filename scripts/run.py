from motion import detectMotion
#from ai import Detector
import cv2

### Add deg

FPS = 10


cap = cv2.VideoCapture("vid.mp4")

ret, frame1 = cap.read()
ret, frame2 = cap.read()
motion = False

while cap.isOpened():
    cv2.imshow("Video", frame1)

    if motion:
          print("motion")

          motion = False
    else:
        #print("no")
        motion = detectMotion(frame1, frame2)

    if cv2.waitKey(50) == ord("q"):
            break
    frame1 = frame2
    ret, frame2 = cap.read()


###
# Logic
# keep 5 second buffer maybe 5-10 frames a second?
# on motion run car/ plate detect on buffer frame 
# keep motion state for 10 seconds
#