from motion import detectMotion
from ai import Detector
import cv2
import time

FPS = 10

cap = cv2.VideoCapture("vid.mp4")
# ret, frame1 = cap.read()
print("aass2" + str(cap.get(cv2.CAP_PROP_FPS)))
ret, frame2 = cap.read()
motion = False
prev = 0
bigBoy = Detector()

while cap.isOpened():
    # time_elapsed = time.time() - prev
    frame1 = frame2
    ret, frame2 = cap.read()

    # if time_elapsed > 1./FPS:
    #     prev = time.time()
    # cv2.imshow("Video", frame1)  # this can be removed

    # if motion:
    #     print("motion")

    #     motion = False
    # else:
    #     # print("no")
    bigBoy.compute(frame1, frame2)

    # if cv2.waitKey(1) == ord("q"):
    #     break  # this can be removed


###
# Logic
# keep 5 second buffer maybe 5-10 frames a second?
# on motion run car/ plate detect on buffer frame
# keep motion state for 10 seconds
#
